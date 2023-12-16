from helpers.exceptions import InputException
from .config import Config


class DefaultConfig(Config):

    def __init__(self, *args):
        super(DefaultConfig, self).__init__(*args)

    def _setMaxImages(self, config, max_images):
        config['default']['max_images'] = max_images

    def _setSorter(self, config, sorter):
        config['default']['sorter'] = sorter

    def _setApiKey(self, config, key):
        config['default']['api_key'] = key

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
