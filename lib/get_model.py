from json import dumps
import requests
import os
from typing import Callable, Dict, List

from lib.utils.utils import write_to_file


def _get_metadata_json(id: str):
    """Returns json object if request succeeds, else print error and returns None"""
    metadata_url = 'https://civitai.com/api/v1/models/' + id
    meta_res = requests.get(metadata_url)
    if meta_res.status_code != 200:
        print(f'Error: Fetching metadata failed ({meta_res.status_code})')
    else:
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
        if image_res.status_code != 200:
            print(
                f'Error: Fetching example images failed ({image_res.status_code})')
        else:
            write_to_file(os.path.join(
                dirpath, os.path.basename(url)), image_res.content, 'wb')


def download_model(model_id: str, create_dir_path: Callable[[Dict, Dict, str, str], str], dst_root_path: str, version_id: str = None, download_image: bool = True, max_img_count: int = 3):
    """
        Downloads the model's safetensors and json metadata files.
        create_dir_path is a callback function that takes in the following: metadata dict, specific model's data as dict, filename, and root path.
    """
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
    if (model_dict == None):
        return print(f'Error: The version id provided does not exist for this model. Available models: {[dict["id"] for dict in model_dict_list]}')

    # Fetch model data
    model_res = requests.get(create_model_url(model_dict['id']))
    if model_res.status_code != 200:
        return print(f"Error: Fetching model failed ({model_res.status_code})")

    # Find filename
    content_disposition = model_res.headers.get('Content-Disposition')
    if (content_disposition == None):
        return print(f"Error: No Content Disposition Available")
    filename = os.path.splitext(
        content_disposition.split('filename=')[-1].strip('"')
    )[0]

    # Write metadata and model data to files
    dst_dir_path = create_dir_path(
        meta_json, model_dict, filename, dst_root_path)
    if not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path)
    write_to_file(
        os.path.join(dst_dir_path, f'{filename}-{model_id}.json'), dumps(meta_json, indent=2))
    write_to_file(
        os.path.join(dst_dir_path, f'{filename}-{model_id}.safetensors'), model_res.content, 'wb')
    if download_image:
        _download_image(
            dst_dir_path, model_dict['images'], meta_json['nsfw'], max_img_count)
