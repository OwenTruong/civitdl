from dataclasses import dataclass
from datetime import datetime
import json
import os
import sys
from typing import Callable, Dict, Iterable, List, Union
import importlib.util
import concurrent.futures
import requests
from tqdm import tqdm

from helpers.styler import Styler
from helpers.exceptions import CustomException, UnexpectedException

_verbose = False


def get_verbose():
    return _verbose


def set_verbose(verbose: bool):
    global _verbose
    _verbose = verbose
    return _verbose


# TODO: what if a specific image have a hard time with getting a response?


def concurrent_request(req_fn, urls, max_workers=16):
    res_list = None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(req_fn, url) for url in urls]
        res_list = [future.result() for future in futures]

    return res_list


def get_progress_bar(total: float, desc: str):
    return tqdm(total=total, desc=desc,
                unit='iB', unit_scale=True)


def write_to_file(filepath: str, content_chunks: Iterable, mode: str = None, use_pb: bool = False, total: float = 0, desc: str = None):
    """Uses content_chunks to write to filepath bit by bit. If use_pb is enabled, it is recommended to set total kwarg to the length of the file to be written."""
    progress_bar = get_progress_bar(total, desc) if use_pb else None
    with open(filepath, mode if mode != None else 'w') as file:
        for content in content_chunks:
            file.write(content)
            if (progress_bar):
                progress_bar.update(len(content))
    if (progress_bar):
        progress_bar.close()


def write_to_files(dirpath: str, basenames: Iterable, contents: Iterable, mode: str = None, use_pb: bool = False, total: float = 0, desc: str = None):
    """Write content to multiple files in dirpath. If use_pb is enabled, it is recommended to set total kwarg to the number of files being written."""
    progress_bar = get_progress_bar(total, desc) if use_pb else None
    for basename, content in zip(basenames, contents):
        filepath = os.path.join(dirpath, basename)
        with open(filepath, mode if mode != None else 'w') as file:
            file.write(content)
            if (progress_bar):
                progress_bar.update(1)
    if (progress_bar):
        progress_bar.close()


def find_in_list(li, cond_fn: Callable[[any, int], bool], default=None):
    """Given a list and a condition function, where the first argument is the index of the item and the second argument is the value of the item, it returns the first value in the list when the condition is true"""
    return next((item for i, item in enumerate(li) if cond_fn(item, int)), default)


def run_verbose(fn, *args, **kwargs):
    if get_verbose():
        fn(*args, **kwargs)


def print_verbose(*args, **kwargs):
    if get_verbose():
        args = [Styler.stylize(arg, bg_color='info') for arg in args]
        print(*args, **kwargs)


def print_exc(exc: Exception, *args, **kwargs):
    if isinstance(exc, CustomException):
        print(exc, file=sys.stderr, *args, **kwargs)
    else:
        print(Styler.stylize(str(exc), color='exception'), *args,
              file=sys.stderr, **kwargs)


def import_sort_model(filepath) -> Callable[[Dict, Dict, str, str], str]:
    spec = importlib.util.spec_from_file_location('sorter', filepath)
    sorter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sorter)
    return sorter.sort_model


def getDate():
    now = datetime.now()
    return now.strftime("%Y-%m-%d--%H:%M:%S-%f")


def createDirsIfNotExist(dirpaths):
    for dirpath in dirpaths:
        os.makedirs(dirpath, exist_ok=True)


@dataclass
class Config:
    sorter: str = 'basic'
    retry_count: int = 3
    pause_time: int = 3

    max_imgs: int = 3
    with_prompt: bool = True
    api_key: Union[str, None] = None

    verbose: Union[bool, None] = None

    def __post_init__(self):
        self.session = requests.Session()

        if self.verbose != None:
            set_verbose(self.verbose)
