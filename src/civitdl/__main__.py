#!/usr/bin/env python3
import traceback
from operator import itemgetter

from helpers.utils import run_in_dev, print_exc
from .batch.batch_download import batch_download, Config
from .args.argparser import get_args


def main():
    try:
        ids, rootdir, sorter, max_imgs, with_prompt, api_key = itemgetter(
            'ids', 'rootdir', 'sorter', 'max_imgs', 'with_prompt', 'api_key')(get_args())

        batch_download(
            ids,
            rootdir=rootdir,
            config=Config(
                sorter=sorter,
                max_imgs=max_imgs,
                with_prompt=with_prompt,
                api_key=api_key
            )
        )

    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print_exc(e)
        print('---------')
