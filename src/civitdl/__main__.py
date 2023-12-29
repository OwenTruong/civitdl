#!/usr/bin/env python3
import traceback
from operator import itemgetter

from helpers.utils import run_verbose, print_exc
from .batch.batch_download import batch_download, Config
from .args.argparser import get_args
from helpers.sourcemanager import SourceManager


def main():
    try:
        print('hi')
        source_strings, rootdir, sorter, max_imgs, with_prompt, api_key, verbose = itemgetter(
            'source_strings', 'rootdir', 'sorter', 'max_imgs', 'with_prompt', 'api_key', 'verbose')(get_args())

        config = Config(
            sorter=sorter,
            max_imgs=max_imgs,
            with_prompt=with_prompt,
            api_key=api_key,
            verbose=verbose
        )

        source_manager = SourceManager()

        batch_download(
            ids=source_manager.parse_src(source_strings),
            rootdir=rootdir,
            config=config
        )

    except Exception as e:
        print('---------')
        run_verbose(traceback.print_exc)
        print_exc(e)
        print('---------')
