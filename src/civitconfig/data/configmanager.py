import glob
import os
import json
import uuid
import shutil
from datetime import datetime

from appdirs import AppDirs

from helpers.exceptions import InputException, ResourcesException, UnexpectedException
from helpers.sorter import basic, tags
from helpers.utils import run_in_dev, import_sort_model

# Check alias -> current dir -> default


class ConfigManager:
    config_path: str
    config_trash_dir_path: str
    sorters_dir_path: str
    sorters_trash_dir_path: str

    def __init__(self):
        dirs = AppDirs('civitdl', 'Owen Truong')
        self.config_path = os.path.join(dirs.user_config_dir, 'config.json')
        self.config_trash_dir_path = os.path.join(
            dirs.user_config_dir, '.trash')
        self.sorters_dir_path = os.path.join(dirs.user_config_dir, 'sorters')
        self.sorters_trash_dir_path = os.path.join(
            self.sorters_dir_path, '.trash')

        # Make sure everything exists #
        os.makedirs(dirs.user_config_dir, exist_ok=True)
        os.makedirs(self.config_trash_dir_path, exist_ok=True)
        os.makedirs(self.sorters_dir_path, exist_ok=True)
        os.makedirs(self.sorters_trash_dir_path, exist_ok=True)
        if not self._configExists():
            self.setFallback()

    ### Low Level ###

    ## Low Level Helper ##

    def _getDate(self) -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d--%H:%M:%S-%f")

    ## Low Level 1 ##

    def _configExists(self):
        return os.path.exists(self.config_path)

    def _getConfig(self):
        data = None

        with open(self.config_path) as file:
            data = json.load(file)
        if data == None:
            raise UnexpectedException('JSON config file was not read...')

        return data

    def _saveConfig(self, dic: dict):
        with open(self.config_path, 'w') as file:
            json.dump(dic, file, indent=2)

    def _trashConfig(self):
        dst_filename = f'{self._getDate()}.json'
        trashpath = os.path.join(
            self.config_trash_dir_path, dst_filename)
        shutil.move(self.config_path, trashpath)
        return trashpath

    def _copyPyFile(self, filepath) -> str:
        dst_filename = f'{self._getDate()}.py'
        dstpath = os.path.join(
            self.sorters_dir_path, dst_filename)
        shutil.copy2(filepath, dstpath)
        return dstpath

    def _uncopyPyFile(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            raise ResourcesException(
                'Unable to uncopy python file (or delete it from program) because it does not exist')

    def _trashPyFile(self, filepath):
        filename = os.path.basename(filepath)
        trashpath = os.path.join(
            self.sorters_trash_dir_path, filename)
        if os.path.exists(filepath):
            shutil.move(filepath, trashpath)
            return trashpath
        else:
            raise ResourcesException(
                'Unable to trash python file because it does not exist.')

    # FIXME: public function is incorrectly providing trash path, in the first place pub is not supposed to know trash path
    def _untrashPyFile(self, trashpath):
        filename = os.path.basename(trashpath)
        filepath = os.path.join(
            self.sorters_dir_path, filename)
        if os.path.exists(trashpath):
            shutil.move(trashpath, filepath)
            return filepath
        else:
            raise ResourcesException(
                'Unable to untrash python file because it does not exist.')

    def _setMaxImages(self, config, max_images):
        config['default']['max_images'] = max_images

    def _setSorter(self, config, sorter):
        config['default']['sorter'] = sorter

    def _setApiKey(self, config, key):
        config['default']['api_key'] = key

    ## Low Level 2 ##

    def _trashPyFiles(self, pyfile_paths):
        trashfile_paths = []
        try:
            for pyfile_path in pyfile_paths:
                trashfile_paths.append(self._trashPyFile(pyfile_path))
            return trashfile_paths
        except Exception as e:
            for trashfile_paths in trashfile_paths:
                self._untrashPyFile(trashfile_paths)
            raise e

    def _untrashPyFiles(self, trashfile_paths):
        pyfile_paths = []
        try:
            for trashfile_path in trashfile_paths:
                pyfile_paths.append(self._untrashPyFile(trashfile_path))
            return pyfile_paths
        except Exception as e:
            for pyfile_path in pyfile_paths:
                self._trashPyFile(pyfile_path)
            raise e

    ### Public Functions ###

    ## Level 1 - No pub dep ##

    def getDefaultAsList(self) -> list:
        return self._getConfig()['default'].values()

    def getSortersList(self) -> list:
        return self._getConfig()['sorters']

    def getAliasesList(self) -> list:
        return self._getConfig()['aliases']

    def setFallback(self):
        fallback = {
            "version": "1.0.0",
            "default": {
                "max_images": 3,
                "sorter": "basic",
                "api_key": ""
            },
            "sorters": [["basic", basic.sort_model.__doc__, 'basic'], ["tags", tags.sort_model.__doc__, 'tags']],
            "aliases": [["@example", "~/.models"]]
        }
        if self._configExists():
            sorters = self.getSortersList()
            try:
                self._trashConfig()
            except Exception as e:
                raise UnexpectedException(
                    'Unable to move config file to trash.', f'\nOriginal Error:\n       {e}')
            try:
                sorter_py_paths = [
                    sorter[2] for sorter in sorters if sorter[0] != 'basic' and sorter[0] != 'tags'
                ]
                self._trashPyFiles(sorter_py_paths)
            except Exception as e:
                raise UnexpectedException(
                    'Unable to move sorters to trash.', f'\n(Original Error)\n       {e}')

        self._saveConfig(fallback)

    ## Level 2 - level 1 pub deps ##

    def setDefault(self, max_images=None, sorter=None, api_key=None):
        config = self._getConfig()
        if max_images:
            if type(max_images) != int or max_images < 0:
                raise InputException(
                    f'max_images argument is not type int or max_images is below 0. The following was provided: {max_images}')
            self._setMaxImages(config, max_images)
        if sorter:
            if len([s for s in self.getSortersList() if s[0] == sorter]) != 1:
                raise InputException(f'Sorter "{sorter}" does not exist')
            self._setSorter(config, sorter)
        if api_key:
            self._setApiKey(config, api_key)
        self._saveConfig(config)

    def addSorter(self, name, filepath):
        sorters = self.getSortersList()

        if name == 'tags' or name == 'basic':
            raise InputException(f'Sorter with name "{name}" is reserved.')

        if '/' in name:
            raise InputException(f'Sorter name may not contain "/": {name}')

        if name in [sorter[0] for sorter in sorters]:
            raise InputException(f'Sorter with name "{name}" already exist.')

        desc = import_sort_model(
            filepath).__doc__ or "Description not provided"

        # First, we save python file (if exception, need to undo)
        filepath = self._copyPyFile(filepath)

        # Then, we edit config
        config = None
        try:
            config = self._getConfig()
            config['sorters'].append([name, desc, filepath])
        except:
            self._uncopyPyFile(filepath)
            raise e

        # Lastly, we save config
        try:
            self._saveConfig(config)
        except Exception as e:
            self._uncopyPyFile(filepath)
            raise e

    def deleteSorter(self, name):
        sorters = self.getSortersList()

        if name == 'tags' or name == 'basic':
            raise InputException(
                f'Sorter with name "{name}" can not be deleted.')

        if name not in [sorter[0] for sorter in sorters]:
            raise InputException(f'Sorter with name "{name}" does not exist.')

        sorter_py_path = [sorter[2]
                          for sorter in sorters if sorter[0] == name][0]

        # First, we edit config
        config = self._getConfig()
        config['sorters'] = [
            sorter for sorter in config['sorters'] if sorter[0] != name]
        if config['default']['sorter'] == name:
            # If default config is the sorter being deleted, change default back to basic
            config['default'] = 'basic'

        # Then, we delete file (if exception, need to undo)
        resources_error_was_raised = False
        trashpath = None
        try:
            trashpath = self._trashPyFile(sorter_py_path)
        except Exception as e:
            if type(e).__name__ == 'ResourcesException':
                print(e)
                resources_error_was_raised = True
            else:
                raise e

        # Lastly, we make changes to config
        try:
            self._saveConfig(config)
        except Exception as e:
            if not resources_error_was_raised:
                self._untrashPyFile(trashpath)
            raise e

    def addAlias(self, alias_name: str, path: str):
        # if alias does not exist, we add
        aliases = self.getAliasesList()

        if '/' in alias_name:
            raise InputException(
                f'Alias name may not contain "/": {alias_name}')

        if alias_name in [aname for aname, _ in aliases]:
            raise InputException(
                f'Alias name exist already: ${alias_name}')

        config = self._getConfig()
        if path.split(os.path.sep)[0] in [aname for aname, _ in aliases]:
            config['aliases'].append([alias_name, path])
        else:
            config['aliases'].append([alias_name, os.path.abspath(path)])

        self._saveConfig(config)

    def deleteAlias(self, alias_name: str):
        aliases = self.getAliasesList()

        if alias_name not in [aname for aname, _ in aliases]:
            raise InputException(
                f'Alias with name {alias_name} does not exist.')

        config = self._getConfig()
        config['aliases'] = [
            alias for alias in config['aliases'] if alias[0] != alias_name
        ]

        self._saveConfig(config)
