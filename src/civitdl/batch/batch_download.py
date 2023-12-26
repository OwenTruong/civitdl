import importlib.util
import itertools
import time
import traceback
from typing import Dict, Union
from dataclasses import dataclass

from ._get_model import download_model

from helpers.styler import Styler
from helpers.utils import Config, get_env, print_exc, print_in_dev, run_in_dev, import_sort_model
from helpers.sorter import basic, tags


def _choose_sorter(sorter_str: str):
    if sorter_str == 'basic' or sorter_str == 'tags':
        return tags.sort_model if sorter_str == 'tags' else basic.sort_model
    else:
        return import_sort_model(sorter_str)


def _pause(sec):
    print_in_dev('Pausing for 3 seconds...')
    time.sleep(sec)
    print_in_dev('Waking up!')


def batch_download(ids, rootdir, config: Config):
    """Batch downloads model from CivitAI one by one."""

    for id in ids:
        iter = 0
        while True:
            try:
                download_model(
                    id=id,
                    dst_root_path=rootdir,
                    create_dir_path=_choose_sorter(config.sorter),
                    config=config
                )
                _pause(config.pause_time)
                break
            except Exception as e:
                print('---------')
                run_in_dev(traceback.print_exc)
                print_exc(e, '\n')
                print('---------')
                _pause(config.pause_time)
                if iter < config.retry_count:
                    print(Styler.stylize(
                        'Retrying to download the current model...', color='info'))
                    iter += 1
                else:
                    print(Styler.stylize(
                        f'Max retry of {config.retry_count} reached. Skipping the current model...', color='info'))
                    break
