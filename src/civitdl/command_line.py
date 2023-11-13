#!/usr/bin/env python3

import sys
import traceback

from .utils import run_in_dev
from .batch_download import batch_download
from .exceptions import InputException


def main():
    try:
        available_actions = ['batchfile', 'batchstr']
        argv = sys.argv[1:]
        if len(argv) == 0:
            raise InputException(
                f'Need to provide arguments -> <action> *<action\'s arguments>.', f'Available actions: {available_actions}'
            )

        if argv[0] == 'batchfile':
            batch_download('batchfile', argv[1:])
        elif argv[0] == 'batchstr':
            batch_download('batchstr', argv[1:])
        else:
            raise InputException(
                f'Unknown action.',
                f'Available actions: {available_actions}'
            )
    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
