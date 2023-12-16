
import os
import json
from datetime import datetime
import shutil

from helpers.sorter import basic, tags
from helpers.exceptions import UnexpectedException
from helpers.utils import getDate

DEFAULT_CONFIG = {
    "version": "1",
    "default": {
        "max_images": 3,
        "sorter": "basic",
        "api_key": ""
    },
    "sorters": [["basic", basic.sort_model.__doc__, 'basic'], ["tags", tags.sort_model.__doc__, 'tags']],
    "aliases": [["@example", "~/.models"]]
}


class Config:

    _config_path: str
    _config_trash_dir_path: str
    _sorters_dir_path: str
    _sorters_trash_dir_path: str

    def __init__(self, config_path, config_trash_dir_path, sorters_dir_path, sorters_trash_dir_path):
        self._config_path = config_path
        self._config_trash_dir_path = config_trash_dir_path
        self._sorters_dir_path = sorters_dir_path
        self._sorters_trash_dir_path = sorters_trash_dir_path

    # Private Methods #

    ## Configs ##

    def _configExists(self):
        return os.path.exists(self._config_path)

    def _getConfig(self):
        data = None

        with open(self._config_path) as file:
            data = json.load(file)
        if data == None:
            raise UnexpectedException('JSON config file was not read...')

        return data

    def _saveConfig(self, dic: dict):
        with open(self._config_path, 'w') as file:
            json.dump(dic, file, indent=2)

    # Public Methods #

    def getDefaultAsList(self) -> list:
        return self._getConfig()['default'].values()

    def getDefaultMaxImages(self):
        return self._getConfig()['default']['max_images']

    def getDefaultSorterName(self):
        return self._getConfig()['default']['sorter']

    def getDefaultApiKey(self):
        return self._getConfig()['default']['api_key']

    def getSortersList(self) -> list:
        return self._getConfig()['sorters']

    def getAliasesList(self) -> list:
        return self._getConfig()['aliases']
