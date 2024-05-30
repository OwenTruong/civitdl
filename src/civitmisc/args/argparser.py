import os
import re
from typing import Dict, List, Union

import argparse

from helpers.core.utils import get_version
from helpers.argparse import PwdAction, ConfirmAction, ColoredArgParser, BooleanOptionalAction

__all__ = ['get_args']


def add_shared_option(par):
    par.add_argument(
        '--with-color', action=BooleanOptionalAction, help='Enable styles like colors, background colors and bold/italized texts.'
    )
    par.add_argument(
        '--verbose', action=BooleanOptionalAction, help='Prints out traceback and other useful information.')
    par.add_argument(
        '-v', '--version', action='version', version=f'civitdl v{get_version()}', help='Prints out the version of the program.'
    )


parser = ColoredArgParser(
    prog='civitmisc',
    description="civitmisc is a cli program for tasks not related to configuration (civitconfig) or downloading model from the API (civitdl)",
    formatter_class=argparse.RawTextHelpFormatter
)


subparsers = parser.add_subparsers(
    dest='subcommand',
    required=True,
    help='Choose one of the following subcommands: cache.')

cache_parser = subparsers.add_parser(
    'cache', help='Cache-related tasks. Currently cache stores file path to models and hashes. The purpose of cache is to ensure the same model is not repeatly downloaded if it already exists locally.')

cache_parser.add_argument('-s', '--scan-model', metavar='DIRPATH', type=str,
                          help='Scans a directory recursively to add path to model files with matching filename to cache.')
add_shared_option(cache_parser)


def get_args():
    parser_result = parser.parse_args()

    return vars(parser_result)
