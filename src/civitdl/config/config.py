
from importlib import resources
import os
import json

from appdirs import AppDirs

from ..helper.exceptions import UnexpectedException


__all__ = ['setupJson']

dirs = AppDirs('civitdl', 'Owen Truong')


def getFallbackJSON():
    data = {
        "max_image": 3,
    }

    return data


def setupJson():
    data = None
    print(__package__)

    try:
        with open(os.path.join(dirs.user_config_dir, 'config.json')) as configfile:
            data = json.load(configfile)
    except:
        if data == None:
            data = getFallbackJson()
