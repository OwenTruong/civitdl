#!/usr/bin/env python3

import sys
import traceback
from operator import itemgetter

from helpers.exceptions import UnexpectedException
from helpers.utils import run_in_dev, add_colors
from civitconfig.args.argparser import get_args
from civitconfig.data.configjson import addAlias, deleteAlias, deleteSorter, getConfig, getDefaultAsList, setDefault, getSortersList, addSorter, getAliasesList


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
            print(add_colors('Default:', 'green'))
            print(add_colors(f'     Max Images:         {max_images}', 'blue'))
            print(add_colors(f'     Sorter:             {sorter}', 'green'))
        elif subcommand == 'sorter':
            if args['add'] != None:
                add_name, add_path = args['add']
                addSorter(add_name, add_path)
            elif args['delete'] != None:
                deleteSorter(args['delete'])

            sortersLi = getSortersList()
            for i, [name, docstr, _] in enumerate(sortersLi):
                color = 'green' if i % 2 == 0 else 'blue'
                print(
                    add_colors(
                        f'Sorter #{i + 1}, "{name}":     {f"{docstr[:300 - 3]}..." if len(docstr) > 300 else docstr}', color)
                )
        elif subcommand == 'alias':
            if args['add'] != None:
                add_name, add_path = args['add']
                addAlias(add_name, add_path)
            elif args['delete'] != None:
                deleteAlias(args['delete'])

            aliasesLi = getAliasesList()
            for i, [alias_name, path] in enumerate(aliasesLi):
                color = 'green' if i % 2 == 0 else 'blue'
                print(
                    add_colors(
                        f'Alias #{i + 1}, "{alias_name}": {path}', color
                    )
                )
        else:
            raise UnexpectedException(
                'Unknown subcommand not caught by argparse')

    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
