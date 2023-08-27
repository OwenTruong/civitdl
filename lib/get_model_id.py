from pathlib import Path
import re


def _get_model_id_paths(paths, regex_str):
    li = []
    for path in paths:
        li += [re.search(regex_str, str(path)).group(0)]
    return li


def get_model_ids_from_dir_path(dirpath):
    filepaths = list(Path(dirpath).glob('**/*.safetensors'))
    return _get_model_id_paths(filepaths, r'\d*(?=\.safetensors$)')
