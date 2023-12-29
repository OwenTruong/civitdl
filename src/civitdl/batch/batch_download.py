import importlib.util
import itertools
import time
import traceback
from typing import Dict, List, Union
from dataclasses import dataclass

from ._get_model import download_model

from helpers.styler import Styler
from helpers.sourcemanager import SourceManager
from helpers.utils import BatchOptions, print_exc, print_verbose, run_verbose, import_sort_model
from helpers.sorter import basic, tags


def _choose_sorter(sorter_str: str):
    if sorter_str == 'basic' or sorter_str == 'tags':
        return tags.sort_model if sorter_str == 'tags' else basic.sort_model
    else:
        return import_sort_model(sorter_str)


def _pause(sec):
    print_verbose('Pausing for 3 seconds...')
    time.sleep(sec)
    print_verbose('Waking up!')


def batch_download(source_strings: List[str], rootdir: str, batchOptions: BatchOptions):
    """Batch downloads model from CivitAI one by one."""

    source_manager = SourceManager()

    for id in source_manager.parse_src(source_strings):

        iter = 0
        while True:
            try:
                download_model(
                    id=id,
                    dst_root_path=rootdir,
                    create_dir_path=_choose_sorter(batchOptions.sorter),
                    batchOptions=batchOptions
                )
                _pause(batchOptions.pause_time)
                break
            except Exception as e:
                print('---------')
                run_verbose(traceback.print_exc)
                print_exc(e, '\n')
                print('---------')
                _pause(batchOptions.pause_time)
                if iter < batchOptions.retry_count:
                    print(Styler.stylize(
                        'Retrying to download the current model...', color='info'))
                    iter += 1
                else:
                    print(Styler.stylize(
                        f'Max retry of {batchOptions.retry_count} reached. Skipping the current model...', color='info'))
                    break
