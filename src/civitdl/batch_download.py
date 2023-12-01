import importlib.util
import time
import traceback
from typing import Dict

from .get_model import download_model
from .helper.utils import run_in_dev

from civitdl.helper.sorter import basic, tags


def choose_sorter(sorter: Dict):
    if sorter['type'] == 'path':
        spec = importlib.util.spec_from_file_location('sorter', sorter['data'])
        sorter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sorter)
        return sorter.sort_model
    else:
        return tags.sort_model if sorter['data'] == 'tags' else basic.sort_model


def batch_download(ids, rootdir, sorter, max_imgs):
    """Batch downloads model from CivitAI one by one."""

    for id in ids:
        try:
            download_model(
                id=id,
                create_dir_path=choose_sorter(sorter),
                dst_root_path=rootdir,
                download_image=True,
                max_img_count=max_imgs)
            run_in_dev(print, 'Pausing for 3 seconds...')
            time.sleep(3)
            run_in_dev(print, 'Waking up!')
        except Exception as e:
            print('---------')
            run_in_dev(traceback.print_exc)
            print(e)
            print('---------')
