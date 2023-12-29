#!/usr/bin/env python3

import sys
import traceback
from operator import itemgetter

from helpers.styler import Styler
from helpers.exceptions import UnexpectedException
from helpers.utils import set_verbose, run_verbose, print_verbose, print_exc
from civitconfig.args.argparser import get_args
from civitconfig.data.configmanager import ConfigManager


def main():
    try:
        args = get_args()
        subcommand = args['subcommand']
        config_manager = ConfigManager()
        if args.verbose:
            set_verbose(True)
        else:
            set_verbose(False)

        print_verbose(args)

        if subcommand == 'default':
            if 'max_images' in args or 'with_prompt' or 'sorter' in args or 'api_key' in args:
                config_manager.setDefault(
                    max_images=args['max_images'], with_prompt=args['with_prompt'], sorter=args['sorter'], api_key=args['api_key'])
            (max_images, with_prompt, sorter, _) = config_manager.getDefaultAsList()
            print(Styler.stylize('Default:', color='main'))
            print(Styler.stylize(
                f'     Max Images:         {max_images}', color='main'))
            print(Styler.stylize(
                f'     With Prompt:        {with_prompt}', color='main'))
            print(Styler.stylize(
                f'     Sorter:             {sorter}', color='main'))
        elif subcommand == 'sorter':
            if args['add'] != None:
                add_name, add_path = args['add']
                config_manager.addSorter(add_name, add_path)
            elif args['delete'] != None:
                config_manager.deleteSorter(args['delete'])

            sortersLi = config_manager.getSortersList()
            for i, [name, docstr, _] in enumerate(sortersLi):
                print(
                    Styler.stylize(
                        f'Sorter #{i + 1}, "{name}":     {f"{docstr[:300 - 3]}..." if len(docstr) > 300 else docstr}', color='main')
                )
        elif subcommand == 'alias':
            if args['add'] != None:
                add_name, add_path = args['add']
                config_manager.addAlias(add_name, add_path)
            elif args['delete'] != None:
                config_manager.deleteAlias(args['delete'])

            aliasesLi = config_manager.getAliasesList()
            for i, [alias_name, path] in enumerate(aliasesLi):
                print(
                    Styler.stylize(
                        f'Alias #{i + 1}, "{alias_name}": {path}', color='main'
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
        run_verbose(traceback.print_exc)
        print_exc(e)
        print('---------')
