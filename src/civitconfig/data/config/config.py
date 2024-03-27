
import os
import json
from datetime import datetime
import shutil
from typing import Dict, List, Union

from helpers.sorter import basic, tags
from helpers.core.utils import Styler, UnexpectedException, getDate, sprint
from helpers.core._validation import Validation

DEFAULT_CONFIG = {
    "version": "1",
    "default": {
        "sorter": "basic",
        "max_images": 3,
        "nsfw_mode": "2",
        "api_key": "",

        "with_prompt": True,
        "without_model": False,
        "limit_rate": '0',
        "retry_count": 3,
        "pause_time": 3.0,

        "cache_mode": '1',
        "model_overwrite": False,

        "with_color": True
    },
    "sorters": [["basic", basic.sort_model.__doc__, 'basic'], ["tags", tags.sort_model.__doc__, 'tags']],
    "aliases": [["@example", "~/.models"]]
}


CURRENT_VERSION = "1"

_config = None  # Do not do async operations with this


class Config:

    _config_path: str
    _config_dir_path: str
    _config_trash_dir_path: str
    _sorters_dir_path: str
    _sorters_trash_dir_path: str

    def __init__(self, config_path, config_dir_path, config_trash_dir_path, sorters_dir_path, sorters_trash_dir_path):
        self._config_path = config_path
        self._config_dir_path = config_dir_path
        self._config_trash_dir_path = config_trash_dir_path
        self._sorters_dir_path = sorters_dir_path
        self._sorters_trash_dir_path = sorters_trash_dir_path

    # Private Methods #

    ## Configs ##

    def _configExists(self):
        return os.path.exists(self._config_path)

    def _getConfig(self):
        global _config
        if not _config:
            with open(self._config_path, encoding='UTF-8') as file:
                _config = json.load(file)
            if _config == None:
                raise UnexpectedException('JSON config file was not read...')

        return _config

    def _saveConfig(self, dic: Dict):
        global _config
        with open(self._config_path, 'w', encoding='UTF-8') as file:
            json.dump(dic, file, indent=2)
            _config = dic

    def _get_valid_keys(self):
        return DEFAULT_CONFIG['default'].keys()

    # Public Methods #

    def getDefault(self, key=None):
        config = self._getConfig()
        if key == None:
            return config['default']
        else:
            Validation.validate_string(key, 'getDefault', min_len=1)
            return config['default'][key]

    def getSortersList(self) -> List:
        return self._getConfig()['sorters']

    def getAliasesList(self) -> List:
        return self._getConfig()['aliases']

    def print_defaults(self):
        blacklisted_keys = ['api_key']
        sprint(Styler.stylize('Default:', color='main'))
        for key, value in self.getDefault().items():
            if key in blacklisted_keys:
                continue
            key = key.replace('_', ' ').title()
            sprint(Styler.stylize(
                f'     {key}:  {"N/A" if str(value) == "" else value}', color='main'))

    def print_sorters(self):
        for i, [name, docstr, _] in enumerate(self.getSortersList()):
            sprint(
                Styler.stylize(
                    f'Sorter #{i + 1}, "{name}":  {f"{docstr[:300 - 3]}..." if len(docstr) > 300 else docstr}', color='main')
            )

    def print_aliases(self):
        for i, [alias_name, path] in enumerate(self.getAliasesList()):
            sprint(
                Styler.stylize(
                    f'Alias #{i + 1}, "{alias_name}":  {path}', color='main'
                )
            )
