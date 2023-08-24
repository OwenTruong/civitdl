from pathlib import Path
import re


def get_lora_ids(paths, regex_str):
    li = []
    for path in paths:
        li += [re.search(regex_str, str(path)).group(0)]
    return li


def getLoraIdsFromDirPath(dirpath):
    filepaths = list(dirpath.glob('**/*.safetensors'))
    return get_lora_ids(filepaths, r'\d*(?=\.safetensors$)')


lora_path = Path(
    '/home/dekomoon/Documents/mnt/data/general/StableDiffusion/stable-diffusion-webui/models/Lora/unfiltered')
