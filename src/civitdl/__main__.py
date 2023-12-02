#!/usr/bin/env python3

import sys
import traceback
from operator import itemgetter


from helpers.utils import run_in_dev
from .batch_download import batch_download
from civitconfig.data.setupJson import setupJson
from .args.argparser import get_args


def main():
    try:
        setupJson()
        ids, rootdir, sorter, max_imgs = itemgetter(
            'ids', 'rootdir', 'sorter', 'max_imgs')(get_args())
        batch_download(ids, rootdir, sorter, max_imgs)

    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
