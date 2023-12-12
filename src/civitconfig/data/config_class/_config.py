
import os
import json
from datetime import datetime

from helpers.exceptions import UnexpectedException


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

    def _getDate(self) -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d--%H:%M:%S-%f")

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
