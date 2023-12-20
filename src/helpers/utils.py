from datetime import datetime
import json
import os
from typing import Callable, Dict, Generator, List, Union, Iterable
import importlib.util
import concurrent.futures
import requests

from tqdm import tqdm
from termcolor import colored

from helpers.exceptions import InputException, UnexpectedException
_environment = 'production'


def get_env():
    return _environment


def set_env(env: str):
    if env != 'production' and env != 'development':
        raise UnexpectedException(
            f'Program is trying to set unexpected enviornment {env}')
    global _environment
    _environment = env
    return _environment


# TODO: what if a specific image have a hard time with getting a response?


def concurrent_request(req_fn, urls):
    res_list = None

    with concurrent.futures.ThreadPoolExecutor() as executor:
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


def run_in_dev(fn, *args):
    if get_env() == 'development':
        fn(*args)


def import_sort_model(filepath) -> Callable[[Dict, Dict, str, str], str]:
    spec = importlib.util.spec_from_file_location('sorter', filepath)
    sorter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sorter)
    return sorter.sort_model


def add_colors(message, color):
    return colored(message, color)


def getDate():
    now = datetime.now()
    return now.strftime("%Y-%m-%d--%H:%M:%S-%f")


def createDirsIfNotExist(dirpaths):
    for dirpath in dirpaths:
        os.makedirs(dirpath, exist_ok=True)
