#!/usr/bin/env python3
import traceback
from operator import itemgetter

from .batch.batch_download import batch_download, BatchOptions
from .args.argparser import get_args

from helpers.exceptions import UnexpectedException
from helpers.sourcemanager import SourceManager
from helpers.utils import print_verbose, run_verbose, print_exc, set_verbose


def main():
    try:
        args = get_args()

        if args['verbose']:
            set_verbose(True)
        else:
            set_verbose(False)

        print_verbose('Arguments: ', str(args))

        batchOptions = BatchOptions(
            sorter=args['sorter'],
            max_imgs=args['max_imgs'],
            with_prompt=args['with_prompt'],
            api_key=args['api_key'],
        )

        batch_download(
            source_strings=args['source_strings'],
            rootdir=args['rootdir'],
            batchOptions=batchOptions
        )

    except Exception as e:
        print('---------')
        run_verbose(traceback.print_exc)
        print_exc(e)
        print('---------')
