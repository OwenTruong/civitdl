#!/usr/bin/env python3

import sys
import traceback
from operator import itemgetter

from helpers.exceptions import UnexpectedException
from helpers.utils import run_in_dev
from civitconfig.args.argparser import get_args
from civitconfig.data.configjson import getConfig, getDefaultAsList, setDefault


def main():
    try:
        args = get_args()
        subcommand = args['subcommand']
        run_in_dev(print, args)

        if subcommand == 'default':
            if 'max_images' in args or 'sorter' in args or 'api_key' in args:
                setDefault(
                    max_images=args['max_images'], sorter=args['sorter'], api_key=args['api_key'])
            (max_images, sorter, _) = getDefaultAsList()
            print(
                f'Defaults:\n      Max Images:     {max_images}\n      Sorter:         {sorter}'
            )
            # TODO: Write the other subcommands
            # TODO: Should I do all of these for loops in args? Yk to separate data...
        elif subcommand == 'sorter':
            print('sorter')
        elif subcommand == 'alias':
            print('alias')
        else:
            raise UnexpectedException(
                'Unknown subcommand not caught by argparse')

    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
