import os
import re
from typing import Dict, List, Union

import argparse

from helpers.styler import Styler
from helpers.exceptions import InputException, UnexpectedException
from helpers.argparse import PwdAction, ConfirmAction, ColoredArgParser
from helpers.utils import get_env, print_in_dev, set_env

__all__ = ['get_args']


def add_shared_option(par):
    par.add_argument(
        '-v', '--dev', action=argparse.BooleanOptionalAction, help='Prints out traceback and other useful information.')


parser = ColoredArgParser(
    prog='civitconfig',
    description="civitconfig is a cli program used to set configurations for the main program, civitdl.",
    formatter_class=argparse.RawTextHelpFormatter
)


subparsers = parser.add_subparsers(
    dest='subcommand',
    required=True,
    help='Choose one of the following subcommands: default, sorter, alias.')

default_parser = subparsers.add_parser(
    'default', help='Set a default value for one of the options below.\nIf no options are provided, default will print the current default.')
default_parser.add_argument('-i', '--max-images', metavar='INT', type=int,
                            help='Set the default max number of images to download per model.')
default_parser.add_argument('-p', '--with-prompt', action=argparse.BooleanOptionalAction,
                            help='Toggles default behavior on whether to download prompt alongside images.')
default_parser.add_argument('-s', '--sorter', metavar='NAME', type=str,
                            help='Set the default sorter given name of sorter (filepath not accepted).')
default_parser.add_argument('-k', '--api-key', action=PwdAction, type=str, nargs=0,
                            help='Prompts the user for their api key to use for model downloads that require users to log in.')
add_shared_option(default_parser)


sorter_parser = subparsers.add_parser(
    'sorter', help='Sorter-related subcommand.\nCurrently supports listing, adding and deleting sorters.\nIf no options are provided, sorter will list all available sorters.\nExample usage: civitdl 123456 ./lora --sorter mysorter.',
    formatter_class=argparse.RawTextHelpFormatter
)
sorter_group = sorter_parser.add_mutually_exclusive_group()
sorter_group.add_argument('-a', '--add', metavar=('NAME', 'FILEPATH'), type=str, nargs=2,
                          help='Add/save a new sorter to civitdl program.\nExample: civitconfig sorter --add mysorter ./custom/tags.py.')
sorter_group.add_argument('-d', '--delete', metavar='NAME', type=str,
                          help='Delete sorter based on name of the sorter.\nExample: civitconfig sorter --delete mysorter.')
add_shared_option(sorter_parser)


alias_parser = subparsers.add_parser(
    'alias',
    help='Alias-related subcommand.\nCurrently supports listing, adding and deleting aliases.\nIf no options are provided, alias will list all available aliases.\nExample usage: civitdl 123456 @lora.',
    formatter_class=argparse.RawTextHelpFormatter
)
alias_group = alias_parser.add_mutually_exclusive_group()
alias_group.add_argument('-a', '--add', metavar=('NAME', 'FILEPATH'), type=str, nargs=2,
                         help='Add a new alias to the civitdl program.\nExample: civitconfig alias --add @lora ./ComfyUI/models/loras.')
alias_group.add_argument('-d', '--delete', metavar=('NAME'), type=str,
                         help='Delete alias based on name of the alias.\nExample: civitconfig alias --delete @lora.')
add_shared_option(alias_parser)


config_parser = subparsers.add_parser(
    'settings',
    help='Subcommand related to the operations of civitconfig.',
    formatter_class=argparse.RawTextHelpFormatter
)
config_group = config_parser.add_mutually_exclusive_group()
config_group.add_argument(
    '-r', '--reset', action=ConfirmAction, help='Delete config and reinstall the default configuration.\nWARNING: DO NOT RUN THIS UNLESS YOU ARE SURE YOU WANT TO DELETE.')
config_group.add_argument(
    '-d', '--download', metavar=('PATH'), type=str, help='Downloads config directory to specified path.')
add_shared_option(config_parser)


def get_args():
    parser_result = parser.parse_args()
    if parser_result.dev:
        set_env('development')

    print_in_dev(f'Parsed Args: {parser_result}')

    return vars(parser_result)
