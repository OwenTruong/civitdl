
from importlib import resources, util
import os
import json
import traceback
import uuid
import shutil

from appdirs import AppDirs

from helpers.exceptions import InputException, ResourcesException, UnexpectedException
from helpers.sorter import basic, tags
from helpers.utils import run_in_dev, import_sort_model


dirs = AppDirs('civitdl', 'Owen Truong')
CONFIG_PATH = os.path.join(dirs.user_config_dir, 'config.json')
SORTERS_DIR_PATH = os.path.join(dirs.user_config_dir, 'sorters')
SORTERS_TRASH_DIR_PATH = os.path.join(SORTERS_DIR_PATH, '.trash')

# Check alias -> current dir -> default
# Example alias -> { "alias": "L", "path": "~/Downloads/ComfyUI/models/loras" }

run_in_dev(print, CONFIG_PATH)


# this is too general compared to savePyFile
def _saveToJSON(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)

    return os.path.basename(path)


def _unsavePyFile(filename):
    if os.path.exists(filename):
        os.remove(os.path.join(SORTERS_DIR_PATH, filename))
    else:
        raise ResourcesException(
            'Unable to unsave python file (or delete it from program) because it does not exist')


def _savePyFile(data) -> str:
    def getRandomDst(): return os.path.join(
        SORTERS_DIR_PATH, f'{str(uuid.uuid4())}.py')

    os.makedirs(SORTERS_DIR_PATH, exist_ok=True)

    dst_path = getRandomDst()
    while os.path.exists(dst_path):
        dst_path = getRandomDst()

    with open(dst_path, 'w') as file:
        file.write(data)

    return os.path.basename(dst_path)


def _trashPyFile(filename):
    os.makedirs(SORTERS_TRASH_DIR_PATH, exist_ok=True)
    pypath = os.path.join(SORTERS_DIR_PATH, filename)
    if os.path.exists(pypath):
        shutil.move(pypath, os.path.join(SORTERS_TRASH_DIR_PATH, filename))


def _untrashPyFile(filename):
    os.makedirs(SORTERS_TRASH_DIR_PATH, exist_ok=True)
    trashpath = os.path.join(SORTERS_TRASH_DIR_PATH, filename)
    if os.path.exists(trashpath):
        shutil.move(trashpath, os.path.join(SORTERS_DIR_PATH, filename))


def _setFallback():
    fallback = {
        "default": {
            "max_image": 3,
            "sorter": "basic",
            "api_key": ""
        },
        "sorters": [["basic", basic.sort_model.__doc__, 'N/A'], ["tags", tags.sort_model.__doc__, 'N/A']],
        "aliases": [["@example", "~/.models"]]
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


### Public Functions ###


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


def getSortersList() -> list:
    return getConfig()['sorters']


def getAliasesList() -> list:
    return getConfig()['aliases']


def setDefault(max_images=None, sorter=None, api_key=None):
    config = getConfig()
    if max_images:
        if type(max_images) != int or max_images < 0:
            raise InputException(
                f'max_images argument is not type int or max_images is below 0. The following was provided: {max_images}')
        config["default"]["max_images"] = max_images
    if sorter:
        if len([s for s in getSortersList() if s[0] == sorter]) != 1:
            raise InputException(f'Sorter "{sorter}" does not exist')
        config["default"]["sorter"] = sorter
    if api_key:
        config["default"]["sorter"] = api_key
    _setConfig(config)


def addSorter(name, filepath):
    sorters = getSortersList()

    if name == 'tags' or name == 'basic':
        raise InputException(f'Sorter with name "{name}" is reserved.')

    for sorter in sorters:
        sname = sorter[0]
        if name == sname:
            raise InputException(f'Sorter with name "{name}" already exist.')

    desc = import_sort_model(filepath).__doc__
    if desc == None:
        raise InputException(
            f'Something went wrong with the filepath provided for the sorter')

    # First, we edit config
    config = getConfig()
    config['sorters'].append([name, desc, filename])

    # Then, we save python file (if exception, need to undo)
    filename = None
    with open(filepath, 'r') as file:
        filename = _savePyFile(file.read())

    # Lastly, we save config
    try:
        _setConfig(config)
    except Exception as e:
        _unsavePyFile(filename)
        raise e


def deleteSorter(name):
    sorters = getSortersList()

    if name == 'tags' or name == 'basic':
        raise InputException(f'Sorter with name "{name}" can not be deleted.')

    target_sorter = None
    for sorter in sorters:
        sname = sorter[0]
        if name == sname:
            target_sorter = sorter

    if target_sorter == None:
        raise InputException(f'Sorter with name "{name}" does not exist.')

    # First, we edit config
    config = getConfig()
    config['sorters'] = [
        sorter for sorter in config['sorters'] if sorter[0] != name]

    # Then, we delete file (if exception, need to undo)
    try:
        _trashPyFile(target_sorter[2])
    except Exception as e:
        exception_type = type(e)
        if exception_type.__name__ == 'ResourcesException':
            print(e)
        else:
            raise e

    # Lastly, we make changes to config
    try:
        _setConfig(config)
    except Exception as e:
        _untrashPyFile(target_sorter[2])
        raise e


def addAlias(alias_name: str, path: str):
    # if alias does not exist, we add
    aliases = getAliasesList()

    for aname, _ in aliases:
        if aname == alias_name:
            raise InputException(f'Alias name exist already: ${alias_name}')

    config = getConfig()
    if os.path.split(path)[0].split(os.path.sep)[0] in [aname for aname, _ in aliases]:
        config['aliases'].append([alias_name, path])
    else:
        config['aliases'].append([alias_name, os.path.abspath(path)])

    _setConfig(config)


def deleteAlias(alias_name: str):
    aliases = getAliasesList()

    target_alias = None
    for aname, _ in aliases:
        if aname == alias_name:
            target_alias = aname

    if target_alias == None:
        raise InputException(f'Alias with name {alias_name} does not exist.')

    config = getConfig()
    config['aliases'] = [
        alias for alias in config['aliases'] if alias[0] != alias_name
    ]

    _setConfig(config)
