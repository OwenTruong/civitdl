from json import dumps
import requests
import os
import re
from typing import Callable, Dict

from termcolor import colored

from .utils import err_400_if_true, err_404_if_true, err_500_if_true, err_501_if_true, err_if_true, write_to_file


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
        err_501_if_true('/api/' in id_string,
                        'API endpoint is not accepted yet')
        self.__id_string = id_string

        if id_string.isdigit():
            self.__id_handler()
        else:
            self.__url_handler()

    def __id_handler(self):
        id = [self.__id_string]
        self.__handler(id)

    def __url_handler(self):
        regex = r'((?<=models\/)\d+)|((?<=modelVersionId=)\d+)'
        id = re.findall(regex, self.__id_string)
        self.__handler(id)

    def __handler(self, id):
        if len(id) == 2:
            self.model_id = id[0]
            self.version_id = id[1]
            self.model_dict = self.__get_model_metadata()
            self.version_dict = self.__get_version_metadata()
        elif len(id) == 1:
            self.model_id = id[0]
            self.model_dict = self.__get_model_metadata()
            err_404_if_true(len(self.model_dict['modelVersions']) == 0,
                            f'No model versions found from model id, {self.model_id}')
            self.version_dict = self.model_dict['modelVersions'][0]
            self.version_id = self.version_dict['id']
        else:
            err_400_if_true(True,
                            f'Incorrect format sent: "{self.__id_string}"')

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
        meta_res = requests.get(url)
        err_if_true(meta_res.status_code != 200,
                    f'Downloading metadata from CivitAI for "{self.__id_string}" failed', meta_res.status_code)
        return meta_res.json()


# def _get_metadata_json(id: str):
#     """Returns json object if request succeeds, else print error and returns None"""
#     metadata_url = 'https://civitai.com/api/v1/models/' + id
#     meta_res = requests.get(metadata_url)
#     err_if_true(meta_res.status_code != 200,
#                 f'Downloading metadata from CivitAI for id, {id}, failed', meta_res.status_code)
#     return meta_res.json()


def _download_image(dirpath: str, images: list[Dict], nsfw: bool, max_img_count):
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
        err_if_true(image_res.status_code != 200,
                    f'Downloading image from CivitAI failed for the url: {url}', image_res.status_code)
        write_to_file(os.path.join(
            dirpath, os.path.basename(url)), image_res.content, 'wb')


def download_model(input_str: str, create_dir_path: Callable[[Dict, Dict, str, str], str], dst_root_path: str, download_image: bool, max_img_count: int):
    """
        Downloads the model's safetensors and json metadata files.
        create_dir_path is a callback function that takes in the following: metadata dict, specific model's data as dict, filename, and root path.
    """
    err_500_if_true(input_str == None or create_dir_path == None or dst_root_path ==
                    None or download_image == None or max_img_count == None, 'download_model received a None type in one of its parameter')

    metadata = Metadata(input_str)

    print(colored(
        f"Now downloading \"{metadata.model_name}\" with model id, {metadata.model_id}, and version id, {metadata.version_id}...", 'blue'))
    model_res = requests.get(metadata.download_url, headers={
                             "Accept-Charset": "utf-16"})
    err_if_true(model_res.status_code != 200,
                f'Downloading model from CivitAI failed for model id, {metadata.model_id}, and version id, {metadata.version_id}', model_res.status_code)

    # Find filename
    # FIXME: Finding filename by content-disposition is not working for UTF-8 characters (i.e. chinese characters). wget is able to retrieve the filename normally.
    content_disposition = model_res.headers.get('Content-Disposition')
    err_404_if_true(content_disposition == None,
                    f'Downloaded model from CivitAI has no content disposition header available.')
    alt_filename = content_disposition.split('filename=')[-1].strip('"')

    # Temporary solution for finding filename
    filename = None
    for file in metadata.version_dict['files']:
        file_version_id = re.search(r'(?<=models\/)\d+', file['downloadUrl'])
        if file_version_id != None and file_version_id.group(0) == metadata.version_id:
            filename = file['name']
            break

    if filename == None:
        err_404_if_true(alt_filename == None,
                        f"Error: Unable to retrieve filename for {metadata.model_name}")
        filename = alt_filename

    # Create empty directory recursively
    filename_without_ext = os.path.splitext(filename)[0]
    dst_dir_path = create_dir_path(
        metadata.model_dict, metadata.version_dict, filename_without_ext, dst_root_path)
    if not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path)

    # Write model to the directory
    model_filetype = 'safetensors'
    json_path = os.path.join(
        dst_dir_path, f'{filename_without_ext}-mid_{metadata.model_id}-vid_{metadata.version_id}.json')
    model_path = os.path.join(
        dst_dir_path, f'{filename_without_ext}-mid_{metadata.model_id}-vid_{metadata.version_id}.{model_filetype}')
    write_to_file(json_path, dumps(
        metadata.model_dict, indent=2, ensure_ascii=False))
    write_to_file(model_path, model_res.content, 'wb')
    if download_image:
        _download_image(
            dst_dir_path, metadata.version_dict['images'], metadata.nsfw, max_img_count)

    print(colored(
        f"Download completed for \"{metadata.model_name}\" with model id, {metadata.model_id}, and version id, {metadata.version_id}: {model_path}", 'green'))


# def download_model(model_id: str, create_dir_path: Callable[[Dict, Dict, str, str], str], dst_root_path: str, version_id: str = None, download_image: bool = True, max_img_count: int = 3):
#     """
#         Downloads the model's safetensors and json metadata files.
#         create_dir_path is a callback function that takes in the following: metadata dict, specific model's data as dict, filename, and root path.
#     """
#     err_500_if_true(model_id == None or create_dir_path == None or dst_root_path ==
#                     None or download_image == None or max_img_count == None, 'download_model received a None type in one of its parameter')

#     def create_model_url(version):
#         return f'https://civitai.com/api/download/models/{version}'

#     # Fetch model metadata
#     meta_json = _get_metadata_json(model_id)
#     if (meta_json == None):
#         return

#     # Find the specific version of the model
#     model_dict_list: list = meta_json['modelVersions']
#     model_dict = model_dict_list[0] if version_id == None else next(
#         (obj for obj in model_dict_list if str(obj['id']) == version_id), None)
#     err_404_if_true(model_dict == None,
#                     f'The version id, {version_id} provided does not exist on CivitAI for the model with model id, {model_id}.\nAvailable version ids: {[dict["id"] for dict in model_dict_list]}')
#     version_id = model_dict['id']

#     # Fetch model data
#     print(colored(
#         f"Now downloading \"{meta_json['name']}\" with model id, {model_id}, and version id, {version_id}...", 'blue'))
#     model_res = requests.get(create_model_url(
#         model_dict['id']), headers={"Accept-Charset": "utf-16"})

#     err_if_true(model_res.status_code != 200,
#                 f'Downloading model from CivitAI failed for model id, {model_id}, and version id, {version_id}', model_res.status_code)

#     # Find filename # FIXME: Finding filename by content-disposition is not working for UTF-8 characters (i.e. chinese characters). wget is able to retrieve the filename normally.
#     content_disposition = model_res.headers.get('Content-Disposition')
#     err_404_if_true(content_disposition == None,
#                     f'Downloaded model from CivitAI has no content disposition header available.')
#     alt_filename = content_disposition.split('filename=')[-1].strip('"')

#     # Temporary solution for finding filename
#     filename = None
#     for file in model_dict['files']:
#         regex_res = re.search(r'/(\d+)$', file['downloadUrl'])
#         if regex_res != None and regex_res.group(0) == model_dict['id']:
#             filename = file['name']
#             break

#     if filename == None:
#         err_404_if_true(alt_filename == None,
#                         f"Error: Unable to retrieve filename for {meta_json['name']}")
#         filename = alt_filename

#     # Write metadata and model data to files
#     filename_without_ext = os.path.splitext(filename)[0]
#     dst_dir_path = create_dir_path(
#         meta_json, model_dict, filename_without_ext, dst_root_path)
#     if not os.path.exists(dst_dir_path):
#         os.makedirs(dst_dir_path)
#     write_to_file(
#         os.path.join(dst_dir_path, f'{filename_without_ext}-{model_id}.json'), dumps(meta_json, indent=2, ensure_ascii=False))
#     write_to_file(
#         os.path.join(dst_dir_path, f'{filename_without_ext}-{model_id}.safetensors'), model_res.content, 'wb')
#     if download_image:
#         _download_image(
#             dst_dir_path, model_dict['images'], meta_json['nsfw'], max_img_count)

#     tensor_full_path = os.path.join(
#         dst_dir_path, f'{filename_without_ext}-{model_id}.safetensors')
#     print(colored(
#         f"Download completed for \"{meta_json['name']}\" with model id, {model_id}, and version id, {version_id}: {tensor_full_path}", 'green'))
