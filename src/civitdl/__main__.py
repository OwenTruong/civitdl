#!/usr/bin/env python3

import sys
import traceback
from operator import itemgetter


from helpers.utils import run_in_dev
from .batch_download import batch_download
from civitconfig.data.configmanager import ConfigManager
from .args.argparser import get_args


def main():
    try:
        ids, rootdir, sorter, max_imgs, api_key = itemgetter(
            'ids', 'rootdir', 'sorter', 'max_imgs', 'api_key')(get_args())

        config_manager = ConfigManager()
        d_max_imgs, d_sorter_name, d_api_key = config_manager.getDefaultAsList()
        sorters = config_manager.getSortersList()
        aliases = config_manager.getAliasesList()

        batch_download(ids, rootdir, sorter, max_imgs,
                       api_key if api_key else d_api_key)

    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
