from json import dumps
import shutil
import requests
import os
import re
from typing import Callable, Dict, List, Union
from math import ceil

from helpers.styler import Styler
from helpers.sourcemanager import Id
from helpers.utils import BatchOptions, delete_file_if_exists, write_to_file, write_to_files, print_verbose, concurrent_request
from helpers.sorter.utils import SorterData
from helpers.exceptions import InputException, ResourcesException, UnexpectedException, APIException
from helpers.validation import Validation
from helpers.hashmanager import HashManager


class Metadata:
    __batchOptions = None
    __id = None

    model_name = None
    model_id = None
    version_id = None
    version_hashes = None

    model_dict = None
    version_dict = None

    nsfw = False
    image_dicts = None
    image_download_urls = None
    model_download_url = None

    def __init__(self, id: Id, batchOptions: BatchOptions):
        self.__id = id
        self.__batchOptions = batchOptions
        self.__handler()

    def __handler(self):
        type = self.__id.type
        ids = self.__id.data

        if type == 'site' and len(ids) == 2:
            self.model_id = ids[0]
            self.version_id = ids[1]
            self.model_dict = self.__get_model_metadata()
            self.version_dict = self.__get_version_metadata()
        elif type == 'id' or (type == 'site' and len(ids) == 1):
            self.model_id = ids[0]
            self.model_dict = self.__get_model_metadata()
            if len(self.model_dict['modelVersions']) == 0:
                raise ResourcesException(
                    f'No model versions found from model id, {self.model_id}')
            self.version_dict = self.model_dict['modelVersions'][0]
            self.version_id = str(self.version_dict['id'])
        elif type == 'api':
            self.version_id = ids[0]
            self.version_dict = self.__get_version_metadata()
            self.model_id = str(self.version_dict['modelId'])
            self.model_dict = self.__get_model_metadata()
        else:
            raise InputException(
                f'Incorrect format sent ({ids}, {type}): "{self.__id.original}"')

        self.model_name = self.model_dict['name']

        self.nsfw = self.model_dict['nsfw']
        self.image_dicts = [
            image_dict for image_dict in self.version_dict['images']
            if self.nsfw or image_dict['nsfw'] == 'None'
        ][0:self.__batchOptions.max_images]
        self.image_download_urls = [image_dict['url']
                                    for image_dict in self.image_dicts]

        self.model_download_url = self.version_dict['downloadUrl']

        self.version_hashes = self.__get_version_hashes(
            self.version_dict, self.model_download_url)

    def __get_version_hashes(self, version_dict, download_url):
        files = version_dict['files']
        hashes = {}
        for file in files:
            if "downloadUrl" in file and file['downloadUrl'] == download_url:
                if isinstance(file['hashes'], dict):
                    hashes = file['hashes']
                else:
                    print(Styler.stylize(
                        'Hashes found in metadata is not a dictionary! There is an error with the API!', color='error'))
                break
        if hashes is {}:
            print(Styler.stylize('Hash not found in metadata.', color='warning'))
        elif "SHA256" not in hashes:
            print(Styler.stylize('SHA256 hash not found.', color='warning'))
        return hashes

    def __get_model_metadata(self):
        """Returns json object if request succeeds, else print error and returns None"""
        metadata_url = f'https://civitai.com/api/v1/models/{self.model_id}'
        return self.__get_metadata(metadata_url)

    def __get_version_metadata(self):
        metadata_url = f'https://civitai.com/api/v1/model-versions/{self.version_id}'
        return self.__get_metadata(metadata_url)

    def __get_metadata(self, url: str):
        print_verbose('Requesting model metadata.')
        print_verbose(f'Metadata API Request URL: {url}')
        meta_res = self.__batchOptions.session.get(url, stream=True)
        print_verbose('Finished requesting model metadata.')
        if meta_res.status_code != 200:
            raise APIException(
                meta_res.status_code, f'Downloading metadata from CivitAI for "{self.__id.original}" failed when trying to request metadata from "{url}"')

        try:
            return meta_res.json()
        except Exception as e:
            raise UnexpectedException(
                'Unable to parse metadata from CivitAI (incorrect format provided by Civitai).', 'CivitAI might be under maintainence.',
                f'\nOriginal Error:\n       {e}')


# TODO: what if a specific image have a hard time with getting a response?


def _download_images(dirpath: str, image_basenames: List[str], image_urls: List[str], batchOptions: BatchOptions):
    def make_req(url): return batchOptions.session.get(url, stream=True)

    # TODO: Change progress bar to be based on time length of request rather than when all the images are fetched and ready to be written.
    os.makedirs(dirpath, exist_ok=True)
    print_verbose('Now requesting images...')
    image_content_chunks_list = [res.iter_content(1024*1024) for res in concurrent_request(
        req_fn=make_req, urls=image_urls)]
    print_verbose('Finished requesting images...')

    if (len(image_content_chunks_list) == 0):
        print(Styler.stylize('No images to download...', color='warning'))
    else:
        write_to_files(dirpath, image_basenames, image_content_chunks_list, mode='wb',
                       use_pb=True, total=len(image_basenames), desc='Images')


def _download_prompts(dirpath: str, basenames: List[str], image_dicts: List[Dict]):
    if len(image_dicts) != 0:
        write_to_files(dirpath, basenames, [dumps(
            image_dict, indent=2, ensure_ascii=False) for image_dict in image_dicts], encoding='UTF-8')


def _download_metadata(dirpath: str, metadata: Metadata):

    model_dict_filename = f'model_dict-mid_{metadata.model_id}-vid_{metadata.version_id}.json'
    model_dict_path = os.path.join(
        dirpath, model_dict_filename)
    os.makedirs(dirpath, exist_ok=True)
    write_to_file(model_dict_path, [dumps(
        metadata.model_dict, indent=2, ensure_ascii=False)], encoding='UTF-8')


def _download_hashes(dirpath: str, filename_no_ext: str, hashes: Dict):
    hashes_dict_path = os.path.join(dirpath, filename_no_ext + '.csv')
    os.makedirs(dirpath, exist_ok=True)
    data = 'hash_name, hash_id\n'
    for key, value in hashes.items():
        data += f'{key}, {value}\n'
    write_to_file(hashes_dict_path, [data.rstrip()], encoding='UTF-8')


def _get_filename_and_model_res(input_str: str, metadata: Metadata, batchOptions: BatchOptions):
    def get_version_file():
        for file in metadata.version_dict['files']:
            file_version_id = re.search(
                r'(?<=models\/)\d+', file['downloadUrl'])
            if file_version_id != None and file_version_id.group(0) == metadata.version_id:
                return file

    # Request model
    print_verbose('Preparing to send download model request...')
    print_verbose(f'Model Download API URL: {metadata.model_download_url}')
    res = batchOptions.session.get(metadata.model_download_url, stream=True)

    if 'reason=download-auth' in res.url:
        api_key_needed = True
        if batchOptions.api_key:
            headers = {
                'Authorization': f'Bearer {batchOptions.api_key}',
            }
            res = batchOptions.session.get(
                metadata.model_download_url, stream=True, headers=headers)
            api_key_needed = 'reason=download-auth' in res.url

        if api_key_needed:
            print_verbose('reason=download-auth status', res.status_code)
            raise InputException(
                'Unable to download this model as it requires a correct API Key. Please head to "civitai.com", go to "Account Settings", then go to "API Keys" section, then add an api key to your account. After that, paste the key to the program.')

    if res.status_code != 200:
        raise APIException(
            res.status_code, f'Downloading model from CivitAI failed for model id, {metadata.model_id}, and version id, {metadata.version_id}')

    # Find filename from content disposition
    version_file = get_version_file()
    content_disposition = res.headers.get('Content-Disposition')
    filename = None

    if content_disposition == None:
        print(Styler.stylize(
            f'Downloaded model from CivitAI has no content disposition header available.', color='warning'))
        filename = f'{metadata.model_name}--{version_file["name"]}'
    else:
        try:
            filename = content_disposition.split(
                'filename=')[-1].strip('"').encode('latin-1').decode('utf-8')
        except UnicodeDecodeError:
            # Alternative solution for finding filename
            filename = f'{metadata.model_name}--{version_file["name"]}'

    if filename == None:
        raise UnexpectedException(
            f'Unable to retrieve filename for {input_str}')

    return (res, filename)


def download_model(id: Id, dst_root_path: str, batchOptions: BatchOptions):
    """
        Downloads the model's safetensors and json metadata files.
        create_dir_path is a callback function that takes in the following: metadata dict, specific model's data as dict, filename, and root path.
    """
    # if id == None or dst_root_path == None:
    #     raise InputException(
    #         '(download_model) Must provide an id, create_dir_path and dst_root_path')

    metadata = Metadata(id, batchOptions)

    print(Styler.stylize(
        f"""Now downloading \"{metadata.model_name}\"...
            - Model ID: {metadata.model_id}
            - Version ID: {metadata.version_id}\n""",
        color='main'))

    model_res, filename = _get_filename_and_model_res(
        id.original, metadata, batchOptions)

    # Create empty directory recursively #
    filename_no_ext, filename_ext = os.path.splitext(filename)
    sorter_data = batchOptions.sorter(
        metadata.model_dict, metadata.version_dict, filename_no_ext, dst_root_path)

    if not isinstance(sorter_data, SorterData):
        raise InputException(
            f'The following sorter, "{batchOptions.sorter_name}", returned the incorrect type.')

    # Write model to the directory #

    # Download metadata
    _download_metadata(sorter_data.metadata_dir_path, metadata)

    # Download images & prompts
    image_basenames = [os.path.basename(url)
                       for url in metadata.image_download_urls]
    prompts_basenames = [
        f'{os.path.splitext(basename)[0]}.json' for basename in image_basenames]

    _download_images(
        sorter_data.image_dir_path, image_basenames, metadata.image_download_urls, batchOptions)
    if batchOptions.with_prompt:
        _download_prompts(sorter_data.prompt_dir_path, prompts_basenames,
                          metadata.image_dicts)

    # Download model & hashes
    os.makedirs(sorter_data.model_dir_path, exist_ok=True)
    model_filename_no_ext = f'{filename_no_ext}-mid_{metadata.model_id}-vid_{metadata.version_id}'

    _download_hashes(sorter_data.model_dir_path,
                     model_filename_no_ext,
                     metadata.version_hashes)

    model_filename = model_filename_no_ext + filename_ext
    model_path = os.path.join(
        sorter_data.model_dir_path, model_filename)

    hash_manager = None
    cached_model_path = None
    if batchOptions.cache_mode is not '0':
        hash_manager = HashManager(metadata.version_id)
        cached_model_path = hash_manager.get_local_model_path()

    if hash_manager and cached_model_path and cached_model_path != model_path:
        print(Styler.stylize(f"""Model already existed at the following path:
            - Path: {cached_model_path}""", color='info'))
        print(Styler.stylize(f"Copying to new path...", color='info'))
        shutil.copy(cached_model_path, model_path)
    else:
        content_chunks = model_res.iter_content(
            ceil(batchOptions.limit_rate / 8)
            if batchOptions.limit_rate is not None and batchOptions.limit_rate is not 0
            else 1024*1024)
        write_to_file(model_path, content_chunks, mode='wb', limit_rate=batchOptions.limit_rate, overwrite=batchOptions.model_overwrite,
                      use_pb=True, total=float(model_res.headers.get('content-length', 0)), desc='Model')

    if hash_manager:
        hash_manager.set_local_model_cache(model_path, metadata.version_hashes)

    print(Styler.stylize(
        f"""\nDownload completed for \"{metadata.model_name}\" 
            - Model ID: {metadata.model_id}
            - Version ID: {metadata.version_id}
            - Path: {model_path}\n""", color='success'))

    print('---------------------------\n')
