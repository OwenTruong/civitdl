from json import dumps
import requests
import os
import re
from typing import Callable, Dict, List

from termcolor import colored

from .utils import write_to_file, write_to_file_with_progress_bar, run_in_dev

from .exceptions import InputException, ResourcesException, UnexpectedException, APIException


class Metadata:
    __id_string = None

    model_name = None
    model_id = None
    version_id = None

    model_dict = None
    version_dict = None

    download_url = None
    images_dict_li = None
    nsfw = False

    def __init__(self, id_string: str):
        self.__id_string = id_string

        if id_string.isdigit():
            self.__id_handler()
        elif "/api/" in id_string:
            self.__api_url_handler()
        else:
            self.__url_handler()

    def __id_handler(self):
        id = [self.__id_string]
        self.__handler(id, 'id')

    def __url_handler(self):
        model_id_regex = r'(?<=models\/)\d+'
        version_id_regex = r'(?<=modelVersionId=)\d+'
        model_id = re.search(model_id_regex, self.__id_string)
        version_id = re.search(version_id_regex, self.__id_string)
        if model_id == None:
            raise InputException(
                f'Incorrect format for the url/id provided: {self.__id_string}')
        model_id = model_id.group(0)
        if model_id == None:
            raise UnexpectedException(
                f'Unknown error while parsing model id for the url/id provided: {self.__id_string}')

        if version_id:
            version_id = version_id.group(0)
            if version_id == None:
                raise UnexpectedException(
                    f'Unknown error while parsing version id for the url/id provided: {self.__id_string}')

            self.__handler([model_id, version_id], 'url')
        else:
            self.__handler([model_id], 'url')

    def __api_url_handler(self):
        version_id_regex = r'(?<=models\/)\d+'
        version_id = re.search(version_id_regex, self.__id_string)
        if version_id == None:
            raise InputException(
                f'Incorrect format for the url provided: {self.__id_string}')
        version_id = version_id.group(0)
        if version_id == None:
            raise UnexpectedException(
                f'Unknown error while parsing version id for the url provided: {self.__id_string}')
        self.__handler([version_id], 'api')

    def __handler(self, ids: List[int], type: str):
        if type == 'url' and len(ids) == 2:
            self.model_id = ids[0]
            self.version_id = ids[1]
            self.model_dict = self.__get_model_metadata()
            self.version_dict = self.__get_version_metadata()
        elif type == 'id' or (type == 'url' and len(ids) == 1):
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
                f'Incorrect format sent ({ids}, {type}): "{self.__id_string}"')

        self.download_url = self.version_dict['downloadUrl']
        self.images_dict_li = self.version_dict['images']
        self.nsfw = self.model_dict['nsfw']
        self.model_name = self.model_dict['name']

    def __get_model_metadata(self):
        """Returns json object if request succeeds, else print error and returns None"""
        metadata_url = 'https://civitai.com/api/v1/models/' + self.model_id
        return self.__get_metadata(metadata_url)

    def __get_version_metadata(self):
        metadata_url = 'https://civitai.com/api/v1/model-versions/' + self.version_id
        return self.__get_metadata(metadata_url)

    def __get_metadata(self, url: str):
        run_in_dev(print, 'Preparing to download model metadata.')
        meta_res = requests.get(url)
        run_in_dev(print, 'Finished downloading model metadata.')
        if meta_res.status_code != 200:
            raise APIException(
                meta_res.status_code, f'Downloading metadata from CivitAI for "{self.__id_string}" failed when trying to request metadata from "{url}"')
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

    for url in image_urls:
        image_res = requests.get(url)
        if image_res.status_code != 200:
            raise APIException(
                image_res.status_code, f'Downloading image from CivitAI failed for the url: {url}')

        write_to_file(os.path.join(
            dirpath, os.path.basename(url)), image_res.content, 'wb')


def _get_filename_and_model_res(input_str: str, metadata: Metadata):
    # Request model
    run_in_dev(print, 'Preparing to download model by reading headers.')
    res = requests.get(metadata.download_url, stream=True)
    run_in_dev(print, 'Finished downloading headers.')

    if res.status_code != 200:
        raise APIException(
            res.status_code, f'Downloading model from CivitAI failed for model id, {metadata.model_id}, and version id, {metadata.version_id}')

    # Find filename from content disposition
    content_disposition = res.headers.get('Content-Disposition')

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


def download_model(input_str: str, create_dir_path: Callable[[Dict, Dict, str, str], str], dst_root_path: str, download_image: bool, max_img_count: int):
    """
        Downloads the model's safetensors and json metadata files.
        create_dir_path is a callback function that takes in the following: metadata dict, specific model's data as dict, filename, and root path.
    """
    if input_str == None or \
            create_dir_path == None or \
            dst_root_path == None or \
            download_image == None or \
            max_img_count == None:
        raise UnexpectedException(
            'download_model received a None type in one of its parameter')

    metadata = Metadata(input_str)

    print(colored(
        f"""Now downloading \"{metadata.model_name}\"...
            - Model ID: {metadata.model_id}
            - Version ID: {metadata.version_id}\n""",
        'blue'))

    model_res, filename = _get_filename_and_model_res(input_str, metadata)

    # Create empty directory recursively
    filename_without_ext, filename_ext = os.path.splitext(filename)
    dst_dir_path = create_dir_path(
        metadata.model_dict, metadata.version_dict, filename_without_ext, dst_root_path)
    if not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path)

    # Write model to the directory
    json_path = os.path.join(
        dst_dir_path, f'{filename_without_ext}-mid_{metadata.model_id}-vid_{metadata.version_id}.json')
    model_path = os.path.join(
        dst_dir_path, f'{filename_without_ext}-mid_{metadata.model_id}-vid_{metadata.version_id}{filename_ext}')
    write_to_file(json_path, dumps(
        metadata.model_dict, indent=2, ensure_ascii=False))
    write_to_file_with_progress_bar(model_path, model_res, 'wb')
    if download_image:
        _download_image(
            dst_dir_path, metadata.version_dict['images'], metadata.nsfw, max_img_count)

    print(colored(
        f"""\nDownload completed for \"{metadata.model_name}\" 
            - Model ID: {metadata.model_id}
            - Version ID: {metadata.version_id}
            - Path: {model_path}\n""", 'green'))

    print('---------------------------\n')
