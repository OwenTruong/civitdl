from json import dumps
from pathlib import Path
import requests
import urllib.request
import sys

from utils.utils import write_to_file


def download_model(id: str):
    url = 'https://civitai.com/api/download/models/' + id
    response = requests.get(url)


def get_model_metadata(id: str):
    metadata_url = 'https://civitai.com/api/v1/models/' + id
    model_url = 'https://civitai.com/api/download/models/' + id

    meta_res = requests.get(metadata_url)
    model_res = requests.get(model_url)

    if (meta_res.status_code != 200):
        print(f'Error: Metadata Status {meta_res.status_code}')
        return
    if (model_res.status_code != 200):
        print(f'Error: Model Status {model_res.status_code}')
        return

    write_to_file('test.json', dumps(meta_res.json()))
    write_to_file('test.safetensors', model_res.content, 'wb')


get_model_metadata(sys.argv[1])
