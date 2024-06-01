#!/usr/bin/env python3

import traceback

from helpers.core.utils import disable_style, UnexpectedException, NotImplementedException, InputException, set_verbose, run_verbose, print_verbose, print_exc, sprint
from helpers.cache import CacheHelper
from civitmisc.args.argparser import get_args

# TODO: Make verbose and no_style similar to each other


def main():
    try:
        args = get_args()
        if args['verbose']:
            set_verbose(True)
        else:
            set_verbose(False)

        if args['with_color'] == False:
            disable_style()

        subcommand = args['subcommand']
        print_verbose(args)

        if subcommand == 'cache':
            if args['scan_model']:
                CacheHelper.scan_models(args['scan_model'])
            else:
                raise InputException('Cache option not provided.')
        else:
            raise UnexpectedException(
                'Unknown subcommand not caught by argparse')

    except Exception as e:
        sprint('---------')
        run_verbose(traceback.print_exc)
        print_exc(e)
        sprint('---------')
