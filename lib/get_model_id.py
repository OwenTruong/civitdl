from pathlib import Path
import re


def _get_model_id_paths(paths, regex_str):
    """Example, some-lora-000010-123456.safetensors. The model id is 123456."""
    li = []
    for path in paths:
        li += [re.search(regex_str, str(path)).group(0)]
    return li


def get_model_ids_from_dir_path(dirpath):
    """Given a directory path, recursively find all of the safetensors file and extract the model id from the filename."""
    filepaths = list(Path(dirpath).glob('**/*.safetensors'))
    return _get_model_id_paths(filepaths, r'\d*(?=\.safetensors$)')


def get_model_ids_from_comma_file(filepath):
    """Given a comma separated textfile, extract all of the model id and optionally version id as a list of list. Each element inside the comma separated txt file can either be a number or a url link."""
    ids = None
    with open(filepath, 'r') as file:
        ids = file.read().strip().split(',')
        ids = [re.findall(r'\d+', id) for id in ids]
        ids = [id for id in ids if len(id) > 0]
    return ids


def get_model_ids_from_comma_str(str):
    """Given a string where id and url are separated by commas, extract the model id and optionally the version id as a list of list."""
    ids = None
    ids = str.split(',')
    ids = [re.findall(r'\d+', id) for id in ids]
    ids = [id for id in ids if len(id) > 0]
    return ids
