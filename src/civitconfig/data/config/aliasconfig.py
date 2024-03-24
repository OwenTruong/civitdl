import os
from helpers.core.utils import InputException
from .config import Config


class AliasConfig(Config):

    def __init__(self, *args):
        super(AliasConfig, self).__init__(*args)

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
