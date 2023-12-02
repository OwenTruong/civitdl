
from importlib import resources
import os
import json
import traceback

from appdirs import AppDirs

from helpers.exceptions import InputException, UnexpectedException
from helpers.sorter import basic, tags
from helpers.utils import run_in_dev


__all__ = ['getConfig']

dirs = AppDirs('civitdl', 'Owen Truong')
CONFIG_PATH = os.path.join(dirs.user_config_dir, 'config.json')

# Check alias -> current dir -> default
# Example alias -> { "alias": "L", "path": "~/Downloads/ComfyUI/models/loras" }

run_in_dev(print, CONFIG_PATH)


def _saveToJSON(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


def _setFallback():
    fallback = {
        "default": {
            "max_image": 3,
            "sorter": "basic",
            "api_key": ""
        },
        "sorter": [("basic", basic.sort_model.__doc__), ("tags", tags.sort_model.__doc__)],
        "aliases": [("@example", "~/.models")]
    }

    os.makedirs(dirs.user_config_dir, exist_ok=True)
    _saveToJSON(CONFIG_PATH, fallback)

    return fallback


def _setConfig(data):
    try:
        _saveToJSON(CONFIG_PATH, data)
    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('JSON config could potentially be corrupted. It is recommended to reinstall the default configuration.')
        print('---------')


def getConfig():
    data = None

    try:
        with open(CONFIG_PATH) as file:
            data = json.load(file)

        if data == None:
            raise UnexpectedException('JSON config file was not read...')
    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
        print('Wiping JSON config and reinstalling defaults...')
        data = _setFallback()

    if data == None:
        raise UnexpectedException('No data returned from fallback')

    return data


def getDefaultAsList() -> list:
    return getConfig()['default'].values()


def setDefault(max_images=None, sorter=None, api_key=None):
    config = getConfig()
    if max_images:
        config["default"]["max_images"] = max_images
    if sorter:
        config["default"]["sorter"] = sorter
    if api_key:
        config["default"]["sorter"] = api_key
    _setConfig(config)
