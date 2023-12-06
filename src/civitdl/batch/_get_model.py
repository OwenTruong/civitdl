from json import dumps
import requests
import os
import re
from typing import Callable, Dict, List, Union

from termcolor import colored

from civitdl.args.argparser import Id
from helpers.utils import write_to_file, write_to_file_with_progress_bar, run_in_dev
from helpers.exceptions import InputException, ResourcesException, UnexpectedException, APIException


class Metadata:
    __id = None

    model_name = None
    model_id = None
    version_id = None

    model_dict = None
    version_dict = None

    download_url = None
    images_dict_li = None
    nsfw = False

    def __init__(self, id: Id):
        self.__id = id
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

        self.download_url = self.version_dict['downloadUrl']
        self.images_dict_li = self.version_dict['images']
        self.nsfw = self.model_dict['nsfw']
        self.model_name = self.model_dict['name']

    def __get_model_metadata(self):
        """Returns json object if request succeeds, else print error and returns None"""
        metadata_url = f'https://civitai.com/api/v1/models/{self.model_id}'
        return self.__get_metadata(metadata_url)

    def __get_version_metadata(self):
        metadata_url = f'https://civitai.com/api/v1/model-versions/{self.version_id}'
        return self.__get_metadata(metadata_url)

    def __get_metadata(self, url: str):
        run_in_dev(print, 'Preparing to download model metadata.')
        meta_res = requests.get(url)
        run_in_dev(print, 'Finished downloading model metadata.')
        if meta_res.status_code != 200:
            raise APIException(
                meta_res.status_code, f'Downloading metadata from CivitAI for "{self.__id.original}" failed when trying to request metadata from "{url}"')
        return meta_res.json()


def _download_image(dirpath: str, images: List[Dict], nsfw: bool, max_img_count):
    image_urls = []

    for dict in images:
        if len(image_urls) == max_img_count:
            break
        if not nsfw and dict['nsfw'] != 'None':
            continue
        else:
            image_urls.append(dict['url'])

    os.makedirs(dirpath, exist_ok=True)
    for url in image_urls:
        image_res = requests.get(url)
        if image_res.status_code != 200:
            raise APIException(
                image_res.status_code, f'Downloading image from CivitAI failed for the url: {url}')

        write_to_file(os.path.join(
            dirpath, os.path.basename(url)), image_res.content, 'wb')


def _download_metadata(dirpath: str, metadata: Metadata):

    model_dict_filename = f'model_dict-mid_{metadata.model_id}-vid_{metadata.version_id}.json'
    model_dict_path = os.path.join(
        dirpath, model_dict_filename)
    os.makedirs(dirpath, exist_ok=True)
    write_to_file(model_dict_path, dumps(
        metadata.model_dict, indent=2, ensure_ascii=False))


def _get_filename_and_model_res(input_str: str, metadata: Metadata, api_key: Union[str, None]):
    # Request model
    run_in_dev(print, 'Preparing to download model by reading headers.')
    download_url = metadata.download_url + \
        (f'?token={api_key}' if api_key else '')
    res = requests.get(download_url, stream=True)
    run_in_dev(print, 'Finished downloading headers.')

    if res.status_code != 200:

        raise APIException(
            res.status_code, f'Downloading model from CivitAI failed for model id, {metadata.model_id}, and version id, {metadata.version_id}')

    # Find filename from content disposition
    content_disposition = res.headers.get('Content-Disposition')

    if 'reason=download-auth' in res.url:
        raise InputException('Unable to download this model as it requires an API Key. Please head to "civitai.com", go to "Account Settings", then go to "API Keys" section, then add an api key to your account. After that, paste the key to the program.')

    if content_disposition == None:
        raise ResourcesException(
            f'Downloaded model from CivitAI has no content disposition header available.')
    filename = None

    try:
        filename = content_disposition.split(
            'filename=')[-1].strip('"').encode('latin-1').decode('utf-8')
    except UnicodeDecodeError:
        # Alternative solution for finding filename
        for file in metadata.version_dict['files']:
            file_version_id = re.search(
                r'(?<=models\/)\d+', file['downloadUrl'])
            if file_version_id != None and file_version_id.group(0) == metadata.version_id:
                filename = file['name']
                break

    if filename == None:
        raise UnexpectedException(
            f'Unable to retrieve filename for {input_str}')

    return (res, filename)


def download_model(id: Id, create_dir_path: Callable[[Dict, Dict, str, str], str], dst_root_path: str, max_img_count: int, api_key: Union[str, None] = None):
    """
        Downloads the model's safetensors and json metadata files.
        create_dir_path is a callback function that takes in the following: metadata dict, specific model's data as dict, filename, and root path.
    """
    if id == None or \
            create_dir_path == None or \
            dst_root_path == None or \
            max_img_count == None:
        raise UnexpectedException(
            'download_model received a None type in one of its parameter')

    metadata = Metadata(id)

    print(colored(
        f"""Now downloading \"{metadata.model_name}\"...
            - Model ID: {metadata.model_id}
            - Version ID: {metadata.version_id}\n""",
        'blue'))

    model_res, filename = _get_filename_and_model_res(
        id.original, metadata, api_key)

    # Create empty directory recursively #
    filename_without_ext, filename_ext = os.path.splitext(filename)
    paths = create_dir_path(
        metadata.model_dict, metadata.version_dict, filename_without_ext, dst_root_path)

    if len(paths) != 3:
        raise InputException(
            'Sorter function provided returned invalid # of paths.')

    model_dir_path, metadata_dir_path, image_dir_path = paths

    # Write model to the directory #

    # Download metadata
    _download_metadata(metadata_dir_path, metadata)

    # Download images
    _download_image(
        image_dir_path, metadata.version_dict['images'], metadata.nsfw, max_img_count)

    # Download file
    os.makedirs(model_dir_path, exist_ok=True)
    model_filename = f'{filename_without_ext}-mid_{metadata.model_id}-vid_{metadata.version_id}{filename_ext}'
    model_path = os.path.join(
        model_dir_path, model_filename)
    write_to_file_with_progress_bar(model_path, model_res, 'wb')

    print(colored(
        f"""\nDownload completed for \"{metadata.model_name}\" 
            - Model ID: {metadata.model_id}
            - Version ID: {metadata.version_id}
            - Path: {model_path}\n""", 'green'))

    print('---------------------------\n')
