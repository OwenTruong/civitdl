from ._config import Config


class DefaultConfig(Config):

    def __init__(self, *args):
        super(DefaultConfig, self).__init__(*args)
