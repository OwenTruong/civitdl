import importlib.util
import itertools
import time
import traceback
from typing import Dict

from ._get_model import download_model
from helpers.utils import get_env, print_in_dev, run_in_dev, import_sort_model
from helpers.sorter import basic, tags


def choose_sorter(sorter_str: str):
    if sorter_str == 'basic' or sorter_str == 'tags':
        return tags.sort_model if sorter_str == 'tags' else basic.sort_model
    else:
        return import_sort_model(sorter_str)


def pause(sec):
    print_in_dev('Pausing for 3 seconds...')
    time.sleep(sec)
    print_in_dev('Waking up!')


def batch_download(ids, rootdir, sorter, max_imgs, with_prompt, api_key=None):
    """Batch downloads model from CivitAI one by one."""

    retry_count = 3
    pause_time = 3

    for id in ids:
        iter = 0
        while True:
            try:
                download_model(
                    id=id,
                    create_dir_path=choose_sorter(sorter),
                    dst_root_path=rootdir,
                    max_img_count=max_imgs,
                    with_prompt=with_prompt,
                    api_key=api_key)
                pause(pause_time)
                break
            except Exception as e:
                print('---------')
                run_in_dev(traceback.print_exc)
                print(e)
                pause(pause_time)
                iter += 1
                if iter < retry_count:
                    print('Retrying to download the current model...')
                else:
                    print(
                        f'Max retry of {retry_count} reached. Skipping the current model...')
                    break
                print('---------')
