
import os
import json
from datetime import datetime
import shutil

from helpers.exceptions import UnexpectedException
from helpers.utils import getDate


class Config:
    config_path: str
    config_trash_dir_path: str
    sorters_dir_path: str
    sorters_trash_dir_path: str

    def __init__(self, config_path, config_trash_dir_path, sorters_dir_path, sorters_trash_dir_path):
        self.config_path = config_path
        self.config_trash_dir_path = config_trash_dir_path
        self.sorters_dir_path = sorters_dir_path
        self.sorters_trash_dir_path = sorters_trash_dir_path

    # Private Methods #

    ## Configs ##

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

    # Public Methods #

    def getDefaultAsList(self) -> list:
        return self._getConfig()['default'].values()

    def getDefaultMaxImages(self):
        return self._getConfig()['default']['max_images']

    def getDefaultSorterName(self):
        return self._getConfig()['default']['sorters']

    def getDefaultApiKey(self):
        return self._getConfig()['default']['api_key']

    def getSortersList(self) -> list:
        return self._getConfig()['sorters']

    def getAliasesList(self) -> list:
        return self._getConfig()['aliases']
