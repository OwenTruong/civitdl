from json import dumps
import requests
import os

from utils.utils import write_to_file


def get_metadata_json(id: str):
    """Returns json object if request succeeds, else print error and returns None"""
    metadata_url = 'https://civitai.com/api/v1/models/' + id
    meta_res = requests.get(metadata_url)
    if (meta_res.status_code != 200):
        print(f'Error: Fetching metadata failed ({meta_res.status_code})')
    else:
        return meta_res.json()


def download_model(dst_dir_path: str, model_id: str, version_id: int = None):
    def create_model_url(version):
        return f'https://civitai.com/api/download/models/{version}'

    # Fetch model metadata
    meta_json = get_metadata_json(model_id)
    if (meta_json == None):
        return

    # Find the specific version of the model
    models_obj: list = meta_json['modelVersions']
    model_obj = models_obj[0] if version_id == None else next(
        (obj for obj in models_obj if obj['id'] == version_id), None)
    if (model_obj == None):
        # return print('Error: The version id provided does not exist for this model')
        return print([obj['id'] for obj in models_obj])

    # Fetch model data
    model_res = requests.get(create_model_url(model_obj['id']))
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
    if not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path)
    write_to_file(
        os.path.join(dst_dir_path, f'{filename}.json'), dumps(meta_json))
    write_to_file(
        os.path.join(dst_dir_path, f'{filename}.safetensors'), model_res.content, 'wb')
