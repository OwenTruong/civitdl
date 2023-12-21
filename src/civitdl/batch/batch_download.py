import importlib.util
import time
import traceback
from typing import Dict

from ._get_model import download_model
from helpers.utils import get_env, run_in_dev, import_sort_model
from helpers.sorter import basic, tags


def choose_sorter(sorter_str: str):
    if sorter_str == 'basic' or sorter_str == 'tags':
        return tags.sort_model if sorter_str == 'tags' else basic.sort_model
    else:
        return import_sort_model(sorter_str)


def batch_download(ids, rootdir, sorter, max_imgs, with_prompt, api_key=None):
    """Batch downloads model from CivitAI one by one."""

    for id in ids:
        try:
            download_model(
                id=id,
                create_dir_path=choose_sorter(sorter),
                dst_root_path=rootdir,
                max_img_count=max_imgs,
                with_prompt=with_prompt,
                api_key=api_key)
            run_in_dev(print, 'Pausing for 3 seconds...')
            time.sleep(3)
            run_in_dev(print, 'Waking up!')
        except Exception as e:
            print('---------')
            run_in_dev(traceback.print_exc)
            print(e)
            print('---------')
