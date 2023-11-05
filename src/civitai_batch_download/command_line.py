#!/usr/bin/env python3

import ast
import sys
from traceback import print_exc
from termcolor import colored

from .utils import err_400_if_true
from .batch_download import batch_download


def main():
    try:
        available_actions = ['batchfile', 'batchstr']
        argv = sys.argv[1:]
        err_400_if_true(len(argv) == 0,
                        f'Error: Need to provide arguments -> <action> *<action\'s arguments>.\nAvailable actions: {available_actions}')

        if argv[0] == 'batchfile':
            batch_download('batchfile', argv[1:])
        elif argv[0] == 'batchstr':
            batch_download('batchstr', argv[1:])
        else:
            err_400_if_true(
                True, TypeError, f'Error: Unknown action.\nAvailable actions: {available_actions}')
    except Exception as e:
        try:
            res = ast.literal_eval(str(e))
            print(
                f"{colored('Status ' + str(res['status']), 'red', attrs=['bold'])}: {colored(res['message'], 'red')}")
        except:
            # TODO: What do we do about error status from civitai's server?
            print_exc(e)
