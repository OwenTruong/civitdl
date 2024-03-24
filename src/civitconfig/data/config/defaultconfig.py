from helpers.core.utils import InputException, UnexpectedException
from helpers.options import DefaultOptions
from .config import Config


class DefaultConfig(Config):

    def __init__(self, *args):
        super(DefaultConfig, self).__init__(*args)

    def __validate_valid_sorter(self, target_sorter_name):
        if len([True for [name, _, _] in self.getSortersList() if name == target_sorter_name]) == 0:
            raise InputException(
                f'Setting the default sorter {target_sorter_name} failed due to being undefined. Run "civitconfig sorter" to check for valid sorters.')

    def setDefault(self, default_options: DefaultOptions):
        config = self._getConfig()
        options = {key: value for key, value in
                   vars(default_options).items() if value is not None}
        valid_keys = self._get_valid_keys()

        for key, value in options.items():
            if key in valid_keys:
                if key == 'sorter':  # special case
                    self.__validate_valid_sorter(value)

                config['default'][key] = value
            else:
                raise UnexpectedException(
                    'Unknown key found while configuring default options!!!')
        self._saveConfig(config)
