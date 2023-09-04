#!/usr/bin/env python3

import sys
from civitai_batch_download.batch_download import batch_download_by_dir, batch_download_by_file, batch_download_by_str


def main():
    available_actions = ['batchdir', 'batchfile', 'batchstr']
    argv = sys.argv[1:]
    if len(argv) == 0:
        return print(f'Error: Need to provide arguments -> <action> *<action\'s arguments>.\nAvailable actions: {available_actions}')

    match argv[0]:
        case 'batchdir':
            batch_download_by_dir(argv[1:])
        case 'batchfile':
            batch_download_by_file(argv[1:])
        case 'batchstr':
            batch_download_by_str(argv[1:])
        case _:
            return print(f'Error: Unknown action.\nAvailable actions: {available_actions}')


main()
