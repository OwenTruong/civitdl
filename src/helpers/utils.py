from datetime import datetime
import json
import os
from typing import Callable, Dict, List
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


def write_to_file(path, content, mode: str = None):
    f = open(path, mode) if mode != None else open(path, 'w')
    f.write(content)
    f.close()


# def write_to_file_with_progress_bar(path, total_size, desc: str = None, mode: str = None):
#     """If downloading files from http requests, make sure to set stream=True in request"""
#     block_size = 1024
#     progress_bar = tqdm(total=total_size, desc=desc, unit='iB', unit_scale=True)
#     with open(path, mode)
#     None

# TODO: what if a specific image have a hard time with getting a response?


def concurrent_request(req_fn, urls):
    res_list = None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(req_fn, url) for url in urls]
        res_list = [future.result() for future in futures]

    return res_list


def write_res_to_file_with_pb(filepath, res, desc: str = None, mode: str = None):
    """Stream must have been enabled -> request.get(url, stream=True)"""
    run_in_dev(print, "(write_res_to_file_with_pb) res.headers.get('content-length', 0)",
               res.headers.get('content-length', 0))

    block_size = 1024
    total_size = int(res.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size, desc=desc,
                        unit='iB', unit_scale=True)
    with open(filepath, mode if mode != None else 'w') as file:
        for data in res.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        raise UnexpectedException(
            'Unexpected error while writing file with progress bar.')


def write_res_list_to_files_with_pb(dirpath, resList, baseNameList, desc: str = None, mode: str = None):
    """Stream must have been enabled -> request.get(url, stream=True)"""
    total_size = len(resList)
    if (total_size == 0):
        raise InputException('Length of files to write is 0.')

    progress_bar = tqdm(total=total_size, desc=desc,
                        unit='iB', unit_scale=True)
    for i, res in enumerate(resList):
        write_to_file(os.path.join(
            dirpath, baseNameList[i]), res.content, mode)
        progress_bar.update(1)
    progress_bar.close()

    if total_size != 0 and progress_bar.n != total_size:
        raise UnexpectedException(
            'Unexpected error while writing file with progress bar.')


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
