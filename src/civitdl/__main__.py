#!/usr/bin/env python3
import traceback
from operator import itemgetter

from helpers.utils import run_in_dev
from .batch.batch_download import batch_download
from .args.argparser import get_args


def main():
    try:
        ids, rootdir, sorter, max_imgs, api_key = itemgetter(
            'ids', 'rootdir', 'sorter', 'max_imgs', 'api_key')(get_args())

        batch_download(
            ids,
            rootdir=rootdir,
            sorter=sorter,
            max_imgs=max_imgs,
            api_key=api_key)

    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
