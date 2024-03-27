#!/usr/bin/env python3

import traceback

from helpers.core.utils import disable_style, UnexpectedException, set_verbose, run_verbose, print_verbose, print_exc, sprint
from helpers.options import DefaultOptions
from civitconfig.args.argparser import get_args
from civitconfig.data.configmanager import ConfigManager

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

        config_manager = ConfigManager()
        subcommand = args['subcommand']
        print_verbose(args)

        if subcommand == 'default':
            args.pop('subcommand')
            config_manager.setDefault(DefaultOptions(
                sorter=args['sorter'],
                max_images=args['max_images'],
                nsfw_mode=args['nsfw_mode'],
                api_key=args['api_key'],
                with_prompt=args['with_prompt'],
                without_model=args['without_model'],
                limit_rate=args['limit_rate'],
                retry_count=args['retry_count'],
                pause_time=args['pause_time'],
                cache_mode=args['cache_mode'],
                model_overwrite=args['model_overwrite'],
                with_color=args['with_color']
            ))
            config_manager.print_defaults()
        elif subcommand == 'sorter':
            if args['add'] != None:
                add_name, add_path = args['add']
                config_manager.addSorter(add_name, add_path)
            elif args['delete'] != None:
                config_manager.deleteSorter(args['delete'])
            config_manager.print_sorters()
        elif subcommand == 'alias':
            if args['add'] != None:
                add_name, add_path = args['add']
                config_manager.addAlias(add_name, add_path)
            elif args['delete'] != None:
                config_manager.deleteAlias(args['delete'])
            config_manager.print_aliases()
        elif subcommand == 'settings':
            if args['reset'] != None:
                config_manager.reset()
            elif args['download'] != None:
                config_manager.download(args['download'])
        else:
            raise UnexpectedException(
                'Unknown subcommand not caught by argparse')

    except Exception as e:
        sprint('---------')
        run_verbose(traceback.print_exc)
        print_exc(e)
        sprint('---------')
