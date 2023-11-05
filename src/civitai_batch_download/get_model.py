from json import dumps
import requests
import os
import re
from typing import Callable, Dict

from termcolor import colored

from .utils import err_404_if_true, err_500_if_true, err_if_true, write_to_file


def _get_metadata_json(id: str):
    """Returns json object if request succeeds, else print error and returns None"""
    metadata_url = 'https://civitai.com/api/v1/models/' + id
    meta_res = requests.get(metadata_url)
    err_if_true(meta_res.status_code != 200,
                f'Downloading metadata from CivitAI for id, {id}, failed', meta_res.status_code)
    return meta_res.json()


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


def download_model(model_id: str, create_dir_path: Callable[[Dict, Dict, str, str], str], dst_root_path: str, version_id: str = None, download_image: bool = True, max_img_count: int = 3):
    """
        Downloads the model's safetensors and json metadata files.
        create_dir_path is a callback function that takes in the following: metadata dict, specific model's data as dict, filename, and root path.
    """
    err_500_if_true(model_id == None or create_dir_path == None or dst_root_path ==
                    None or download_image == None or max_img_count == None, 'download_model received a None type in one of its parameter')

    def create_model_url(version):
        return f'https://civitai.com/api/download/models/{version}'

    # Fetch model metadata
    meta_json = _get_metadata_json(model_id)
    if (meta_json == None):
        return

    # Find the specific version of the model
    model_dict_list: list = meta_json['modelVersions']
    model_dict = model_dict_list[0] if version_id == None else next(
        (obj for obj in model_dict_list if str(obj['id']) == version_id), None)
    err_404_if_true(model_dict == None,
                    f'The version id, {version_id} provided does not exist on CivitAI for the model with model id, {model_id}.\nAvailable version ids: {[dict["id"] for dict in model_dict_list]}')
    version_id = model_dict['id']

    # Fetch model data
    print(colored(
        f"Now downloading \"{meta_json['name']}\" with model id, {model_id}, and version id, {version_id}...", 'blue'))
    model_res = requests.get(create_model_url(
        model_dict['id']), headers={"Accept-Charset": "utf-16"})

    err_if_true(model_res.status_code != 200,
                f'Downloading model from CivitAI failed for model id, {model_id}, and version id, {version_id}', model_res.status_code)

    # Find filename # FIXME: Finding filename by content-disposition is not working for UTF-8 characters (i.e. chinese characters). wget is able to retrieve the filename normally.
    content_disposition = model_res.headers.get('Content-Disposition')
    err_404_if_true(content_disposition == None,
                    f'Downloaded model from CivitAI has no content disposition header available.')
    alt_filename = content_disposition.split('filename=')[-1].strip('"')

    # Temporary solution for finding filename
    filename = None
    for file in model_dict['files']:
        regex_res = re.search(r'/(\d+)$', file['downloadUrl'])
        if regex_res != None and regex_res.group(0) == model_dict['id']:
            filename = file['name']
            break

    if filename == None:
        err_404_if_true(alt_filename == None,
                        f"Error: Unable to retrieve filename for {meta_json['name']}")
        filename = alt_filename

    # Write metadata and model data to files
    filename_without_ext = os.path.splitext(filename)[0]
    dst_dir_path = create_dir_path(
        meta_json, model_dict, filename_without_ext, dst_root_path)
    if not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path)
    write_to_file(
        os.path.join(dst_dir_path, f'{filename_without_ext}-{model_id}.json'), dumps(meta_json, indent=2, ensure_ascii=False))
    write_to_file(
        os.path.join(dst_dir_path, f'{filename_without_ext}-{model_id}.safetensors'), model_res.content, 'wb')
    if download_image:
        _download_image(
            dst_dir_path, model_dict['images'], meta_json['nsfw'], max_img_count)

    print(colored(
        f"Download completed for \"{meta_json['name']}\" with model id, {model_id}, and version id, {version_id}...", 'green'))
