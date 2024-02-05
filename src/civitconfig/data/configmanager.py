import os
import shutil

from helpers.core.utils import Styler, UnexpectedException, getDate, print_verbose, sprint
from helpers.options import DefaultOptions
from helpers.core.iohelper import IOHelper
from helpers.core.constants import app_dirs

from .config.config import Config, DEFAULT_CONFIG
from .config.aliasconfig import AliasConfig
from .config.defaultconfig import DefaultConfig
from .config.sorterconfig import SorterConfig

# Check alias -> current dir -> default


class ConfigManager(Config):
    '''ConfigManager is a class that is in charge of the whole configuration. It is also the police that is in charge of making sure all of the subconfigs integrate with each other.'''
    _aliasConfig: AliasConfig
    _defaultConfig: DefaultConfig
    _sorterConfig: SorterConfig

    def __init__(self):
        config_path = os.path.join(app_dirs.user_config_dir, 'config.json')
        config_trash_dir_path = os.path.join(
            app_dirs.user_config_dir, '.trash')
        sorters_dir_path = os.path.join(app_dirs.user_config_dir, 'sorters')
        sorters_trash_dir_path = os.path.join(
            sorters_dir_path, '.trash')
        args = [config_path, app_dirs.user_config_dir, config_trash_dir_path,
                sorters_dir_path, sorters_trash_dir_path]

        print_verbose(f'Config Directory: {app_dirs.user_config_dir}')

        super(ConfigManager, self).__init__(*args)
        self._aliasConfig = AliasConfig(*args)
        self._defaultConfig = DefaultConfig(*args)
        self._sorterConfig = SorterConfig(*args)

        # Make sure all directories exist
        IOHelper.createDirsIfNotExist(args[1:])

        # make sure config file exist
        if not self._configExists():
            self._setFallback()

    def _trashConfig(self):
        dst_filename = f'{getDate()}.json'
        trashpath = os.path.join(
            self._config_trash_dir_path, dst_filename)
        shutil.move(self._config_path, trashpath)
        return trashpath

    def _setFallback(self):
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
                self._sorterConfig.trashPyFiles(sorter_py_paths)
            except Exception as e:
                raise UnexpectedException(
                    'Unable to move sorters to trash.', f'\n(Original Error)\n       {e}')

        self._saveConfig(DEFAULT_CONFIG)

    def setDefault(self, default_options: DefaultOptions):
        self._defaultConfig.setDefault(
            default_options)

    def addAlias(self, alias_name: str, path: str):
        self._aliasConfig.addAlias(alias_name, path)

    def deleteAlias(self, alias_name: str):
        self._aliasConfig.deleteAlias(alias_name)

    def addSorter(self, name, filepath):
        self._sorterConfig.addSorter(name, filepath)

    def deleteSorter(self, name):
        self._sorterConfig.deleteSorter(name)
        default_sorter_name = self.getDefault('sorter')
        sprint(default_sorter_name, name)
        if (default_sorter_name == name):
            self._defaultConfig.setDefault(DefaultOptions(sorter='basic'))

    def reset(self):
        self._setFallback()
        sprint(Styler.stylize('Successfully resetted config.', color='success'))

    def download(self, dst_path):
        if os.path.isdir(dst_path):
            dst_path = os.path.join(dst_path, 'civitdl_config')

        sprint(Styler.stylize(
            f'Downloading zipped config to {dst_path}.zip', color='main'))
        shutil.make_archive(dst_path, 'zip',
                            self._config_dir_path)
