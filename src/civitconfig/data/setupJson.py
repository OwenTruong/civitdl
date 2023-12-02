
from importlib import resources
import os
import json

from appdirs import AppDirs

from helpers.exceptions import UnexpectedException


__all__ = ['setupJson']

dirs = AppDirs('civitdl', 'Owen Truong')
CONFIG_PATH = os.path.join(dirs.user_config_dir, 'config.json')

# Check alias -> current dir -> default
# Example alias -> { "alias": "L", "path": "~/Downloads/ComfyUI/models/loras" }


def getFallback():
    data = {
        "max_image": 3,
        "default_filter": "basic",
        "default_path": '',
        "aliases": []
    }

    if not os.path.exists(dirs.user_config_dir):
        os.makedirs(dirs.user_config_dir)

    with open(CONFIG_PATH, 'w') as file:
        json.dump(data, file, indent=2)

    return data


def setupJson():
    data = None

    try:
        with open(CONFIG_PATH) as file:
            data = json.load(file)

        if data == None:
            raise UnexpectedException('JSON config file was not read')
    except:
        data = getFallback()

    if data == None:
        raise UnexpectedException('No data returned from fallback')

    return data
