#!/usr/bin/env python3

import sys
import traceback
from operator import itemgetter

from helpers.exceptions import UnexpectedException
from helpers.utils import run_in_dev, print_in_dev, add_colors
from civitconfig.args.argparser import get_args
from civitconfig.data.configmanager import ConfigManager


def main():
    try:
        args = get_args()
        subcommand = args['subcommand']
        config_manager = ConfigManager()
        print_in_dev(args)

        if subcommand == 'default':
            if 'max_images' in args or 'with_prompt' or 'sorter' in args or 'api_key' in args:
                print(args['with_prompt'])
                config_manager.setDefault(
                    max_images=args['max_images'], with_prompt=args['with_prompt'], sorter=args['sorter'], api_key=args['api_key'])
            (max_images, with_prompt, sorter, _) = config_manager.getDefaultAsList()
            print(add_colors('Default:', 'green'))
            print(add_colors(f'     Max Images:         {max_images}', 'blue'))
            print(add_colors(
                f'     With Prompt:        {with_prompt}', 'green'))
            print(add_colors(f'     Sorter:             {sorter}', 'blue'))
        elif subcommand == 'sorter':
            if args['add'] != None:
                add_name, add_path = args['add']
                config_manager.addSorter(add_name, add_path)
            elif args['delete'] != None:
                config_manager.deleteSorter(args['delete'])

            sortersLi = config_manager.getSortersList()
            for i, [name, docstr, _] in enumerate(sortersLi):
                color = 'green' if i % 2 == 0 else 'blue'
                print(
                    add_colors(
                        f'Sorter #{i + 1}, "{name}":     {f"{docstr[:300 - 3]}..." if len(docstr) > 300 else docstr}', color)
                )
        elif subcommand == 'alias':
            if args['add'] != None:
                add_name, add_path = args['add']
                config_manager.addAlias(add_name, add_path)
            elif args['delete'] != None:
                config_manager.deleteAlias(args['delete'])

            aliasesLi = config_manager.getAliasesList()
            for i, [alias_name, path] in enumerate(aliasesLi):
                color = 'green' if i % 2 == 0 else 'blue'
                print(
                    add_colors(
                        f'Alias #{i + 1}, "{alias_name}": {path}', color
                    )
                )
        elif subcommand == 'settings':
            if args['reset'] != None:
                config_manager.reset()
            elif args['download'] != None:
                config_manager.download(args['download'])
        else:
            raise UnexpectedException(
                'Unknown subcommand not caught by argparse')

    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
