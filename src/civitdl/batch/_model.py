from json import dumps, loads
import shutil
import os
import re
from typing import Dict, List, Union
from math import ceil

import requests

from helpers.core.utils import Styler, InputException, UnexpectedException, APIException, print_newlines, sprint, print_verbose, concurrent_request
from helpers.core.iohelper import IOHelper

from helpers.sourcemanager import Id
from helpers.options import BatchOptions
from helpers.hashmanager import HashManager

from ._metadata import Metadata


class Model:
    __id: Id
    __dst_root_path: str
    __batchOptions: BatchOptions

    def __init__(self, id: Id, dst_root_path: str, batchOptions: BatchOptions):
        self.__id = id
        self.__dst_root_path = dst_root_path
        self.__batchOptions = batchOptions

    def __download_images(self, dirpath: str, urls: List[str], filenames: List[str]):
        def make_req(url): return self.__batchOptions.session.get(
            url, stream=True)

        # TODO: Change progress bar to be based on time length of request rather than when all the images are fetched and ready to be written.
        # TODO: what if a specific image have a hard time with getting a response?

        os.makedirs(dirpath, exist_ok=True)
        print_verbose('Now requesting images...')
        image_content_chunks_list = [res.iter_content(1024*1024) for res in concurrent_request(
            req_fn=make_req, urls=urls)]
        print_verbose('Finished requesting images...')

        if (len(image_content_chunks_list) == 0):
            sprint(Styler.stylize('No images to download...', color='warning'))
        else:
            IOHelper.write_to_files(dirpath, filenames, image_content_chunks_list, mode='wb',
                                    use_pb=True, total=len(filenames), desc='Images')

    def __download_prompt(self, dirpath: str, filenames: List[str], prompts: List[Dict]):
        if len(prompts) != 0:
            os.makedirs(dirpath, exist_ok=True)
            IOHelper.write_to_files(dirpath, filenames, [dumps(
                image_dict, indent=2, ensure_ascii=False) for image_dict in prompts], encoding='UTF-8')

    def __download_metadata(self, dirpath: str, filename: str, metadata: Metadata):
        os.makedirs(dirpath, exist_ok=True)
        filepath = os.path.join(dirpath, filename)
        IOHelper.write_to_file(filepath, [dumps(
            metadata.model_dict, indent=2, ensure_ascii=False)], encoding='UTF-8')

    def __download_hash(self, dirpath: str, filename: str, hashes: Dict):
        os.makedirs(dirpath, exist_ok=True)
        filepath = os.path.join(dirpath, filename)
        data = 'hash_name, hash_id\n'
        for key, value in hashes.items():
            data += f'{key}, {value}\n'
        IOHelper.write_to_file(
            filepath, [data.rstrip()], encoding='UTF-8')

    def __download_model(self, dirpath, filename: str, model_res: requests.Response, metadata: Metadata):
        os.makedirs(dirpath, exist_ok=True)
        filepath = os.path.join(dirpath, filename)
        hash_manager = HashManager(
            metadata.version_id) if self.__batchOptions.cache_mode != '0' else None
        cached_filepath = hash_manager.get_local_model_path() if hash_manager else None

        if cached_filepath and cached_filepath != os.path.abspath(filepath):
            print_newlines(Styler.stylize(f"""Model already existed at the following path:
                - Path: {cached_filepath}""", color='info'))
            sprint(Styler.stylize(f"Copying to new path...", color='info'))
            shutil.copy(cached_filepath, filepath)
        else:
            content_chunks = model_res.iter_content(
                ceil(self.__batchOptions.limit_rate / 8)
                if self.__batchOptions.limit_rate is not None and self.__batchOptions.limit_rate != 0
                else 1024*1024)
            IOHelper.write_to_file(filepath, content_chunks, mode='wb', limit_rate=self.__batchOptions.limit_rate,
                                   overwrite=self.__batchOptions.model_overwrite, use_pb=True, total=float(model_res.headers.get('content-length', 0)), desc='Model')
        if hash_manager:
            hash_manager.set_local_model_cache(
                filepath, metadata.version_hashes)

    def __request_model(self, metadata: Metadata):
        # Request model
        print_verbose('Preparing to send download model request...')
        print_verbose(f'Model Download API URL: {metadata.model_download_url}')

        headers = {
            'Authorization': f'Bearer {self.__batchOptions.api_key}',
        }
        res = self.__batchOptions.session.get(
            metadata.model_download_url, stream=True, headers=headers)

        print_verbose(f'Status Code: {res.status_code}')

        if 'reason=download-auth' in res.url or res.status_code == 401:
            print_verbose('Unauthorized status', res.url,  res.status_code)
            raise InputException(
                'Unable to download this model as it requires a valid API Key. Please head to "civitai.com", go to "Account Settings", then go to "API Keys" section, then add an api key to your account. After that, paste the key to the program or add it to civitconfig with "civitconfig default --api-key".')

        if res.status_code == 403:
            sprint(Styler.stylize(
                'Model is behind CivitAI\'s early access restriction (i.e have to wait a few days for model to be available to be downloaded).', color='warning'))
            try:
                data = loads(res.content)
                sprint(Styler.stylize(f'Deadline: {data["deadline"]}', color='warning'))  # nopep8
                sprint(Styler.stylize(f'Error Message: {data["message"]}', color='warning'))  # nopep8
            except:
                None
        if res.status_code != 200:
            raise APIException(
                res.status_code, f'Downloading model from CivitAI failed for model id, {metadata.model_id}, and version id, {metadata.version_id}')

        return res

    def __get_filenames(self, metadata: Metadata, content_disposition: Union[str, None] = None):
        def get_api_filename():
            version_file = None
            for file in metadata.version_dict['files']:
                file_version_id = re.search(
                    r'(?<=models\/)\d+', file['downloadUrl'])
                if file_version_id != None and file_version_id.group(0) == metadata.version_id:
                    version_file = file
            filename = None

            if content_disposition == None:
                sprint(Styler.stylize(
                    f'Downloaded model from CivitAI has no content disposition header available.', color='warning'))
                filename = f'{metadata.model_name}--{version_file["name"]}'
            else:
                try:
                    filename = content_disposition.split(
                        'filename=')[-1].strip('"').encode('latin-1').decode('utf-8')
                except UnicodeDecodeError as e:
                    # Alternative solution for finding filename
                    sprint(Styler.stylize(e, color='warning'))
                    filename = f'{metadata.model_name}--{version_file["name"]}'

            if filename == None:
                raise UnexpectedException(
                    f'Unable to retrieve filename for model with model id, {metadata.model_id}, and version id, {metadata.version_id}')

            return filename

        # get filename of metadata
        metadata_filename = f'model_dict-mid_{metadata.model_id}-vid_{metadata.version_id}.json'  # nopep8
        # get filename of images
        image_filenames = [os.path.basename(url)
                           for url in metadata.image_download_urls]
        # get filename of prompts
        prompt_filenames = [
            f'{os.path.splitext(basename)[0]}.json' for basename in image_filenames]
        # get model_stem and model_ext
        model_stem, model_ext = os.path.splitext(get_api_filename())

        # get filename of model
        model_filename = f'{model_stem}-mid_{metadata.model_id}-vid_{metadata.version_id}{model_ext}'  # nopep8

        # get filename of hash
        hash_filename = f'{model_stem}-mid_{metadata.model_id}-vid_{metadata.version_id}.csv'  # nopep8

        return {
            'metadata': metadata_filename,
            'images': image_filenames,
            'prompts': prompt_filenames,
            'model': model_filename,
            'hash': hash_filename
        }

    def download(self):
        # 1. Get metadata
        metadata = Metadata(self.__id, self.__batchOptions).make_api_call()

        print_newlines(Styler.stylize(
            f"""Now downloading \"{metadata.model_name}\"...
                - Model ID: {metadata.model_id}
                - Version ID: {metadata.version_id}\n""",
            color='main'))

        # 2. Get directory and file paths

        model_res = self.__request_model(
            metadata) if not self.__batchOptions.without_model else None

        filenames = self.__get_filenames(
            metadata, model_res.headers.get('Content-Disposition') if model_res else None)

        sorter_data = self.__batchOptions.sorter(
            metadata.model_dict, metadata.version_dict, os.path.split(filenames['model'])[0], self.__dst_root_path)

        # 3. Download model and etc.

        self.__download_metadata(
            sorter_data.metadata_dir_path, filenames['metadata'], metadata)
        self.__download_images(sorter_data.image_dir_path,
                               metadata.image_download_urls, filenames['images'])
        if self.__batchOptions.with_prompt:  # FIXME: I don't like how one of them is with_prompt, and the other is without_model
            self.__download_prompt(
                sorter_data.prompt_dir_path, filenames['prompts'], metadata.image_dicts)
        if not self.__batchOptions.without_model:
            self.__download_model(sorter_data.model_dir_path,
                                  filenames['model'], model_res, metadata)
        self.__download_hash(sorter_data.model_dir_path,
                             filenames['hash'], metadata.version_hashes)

        print_newlines(Styler.stylize(
            f"""\nDownload completed for \"{metadata.model_name}\"
                - Model ID: {metadata.model_id}
                - Version ID: {metadata.version_id}
                - Model Directory Path: {sorter_data.model_dir_path if not self.__batchOptions.without_model else 'N/A'}
                - Hashes Directory Path: {sorter_data.model_dir_path}
                - Metadata Directory Path: {sorter_data.metadata_dir_path}
                - Images Directory Path: {sorter_data.image_dir_path}
                - Images Metadata Directory Path: {sorter_data.prompt_dir_path if self.__batchOptions.with_prompt else 'N/A'}\n""", color='success'))
        sprint('---------------------------\n')

        return self
