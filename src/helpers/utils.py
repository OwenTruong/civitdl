from dataclasses import InitVar, dataclass, field
from datetime import datetime
import json
import os
import sys
import pkg_resources
from typing import Callable, Dict, Iterable, List, Union
import importlib.util
import concurrent.futures
import requests
from tqdm import tqdm

from helpers.sorter.utils import import_sort_model
from helpers.sorter import basic, tags
from helpers.styler import Styler
from helpers.exceptions import CustomException, InputException, UnexpectedException

# Level 0

_verbose = False


def get_verbose():
    return _verbose


def set_verbose(verbose: bool):
    global _verbose
    _verbose = verbose
    return _verbose


def getDate():
    now = datetime.now()
    return now.strftime("%Y-%m-%d--%H:%M:%S-%f")


def get_version():
    return pkg_resources.get_distribution('civitdl').version


# Level 1 - Currently or in the future might depends on level 0


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


def safe_run(callback: Callable[..., any], *values: any) -> dict:
    try:
        return {"success": True, "data": callback(*values)}
    except Exception as e:
        return {"success": False, "error": e}


def concurrent_request(req_fn, urls, max_workers=16):
    res_list = None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(req_fn, url) for url in urls]
        res_list = [future.result() for future in futures]

    return res_list


def get_progress_bar(total: float, desc: str):
    return tqdm(total=total, desc=desc,
                unit='iB', unit_scale=True)


def find_in_list(li, cond_fn: Callable[[any, int], bool], default=None):
    """Given a list and a condition function, where the first argument is the index of the item and the second argument is the value of the item, it returns the first value in the list when the condition is true"""
    return next((item for i, item in enumerate(li) if cond_fn(item, int)), default)


def createDirsIfNotExist(dirpaths):
    for dirpath in dirpaths:
        os.makedirs(dirpath, exist_ok=True)


# Level 2 - Currently or in the future might depends on level 0 and 1


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


# Level 3 - Currently or in the future might depends on level 0, 1 and 2

class BatchOptions:
    retry_count: int = 3
    pause_time: int = 3

    max_imgs: int = 3
    with_prompt: bool = True
    api_key: Union[str, None] = None

    verbose: Union[bool, None] = None

    sorter: Callable[[Dict, Dict, str, str],
                     List[str]] = basic.sort_model

    limit_rate: int = 0

    def __get_sorter(self, sorter: str):
        if not isinstance(sorter, property) and not isinstance(sorter, str):
            raise InputException(
                'Sorter provided is not a string in BatchOptions.')

        sorter_str = 'basic' if isinstance(sorter, property) else sorter
        if sorter_str == 'basic' or sorter_str == 'tags':
            self._sorter = tags.sort_model if sorter_str == 'tags' else basic.sort_model
        else:
            self._sorter = import_sort_model(sorter_str)

        print_verbose("Chosen Sorter Description: ", self._sorter.__doc__)
        return self._sorter

    def __parse_bytes(self, size: Union[str, int, float], arg_name: str):
        units = {"k": 10**3, "m": 10**6, "g": 10**9, "t": 10**12}

        def validate_positive_bytes(number: int) -> None:
            if number <= 0:
                raise InputException(
                    f'({arg_name}) Bytes cannot be zero or negative: {size}')

        res = safe_run(float, size)
        if res["success"] == True:
            number = round(res["data"])
            validate_positive_bytes(number)
            return number
        else:
            number, unit = (size[0:-1], size[-1:].lower())

            num_res = safe_run(float, number)
            if num_res["success"] == False:
                raise InputException(
                    f'({arg_name}) Invalid byte value: {size}')
            else:
                number = round(num_res["data"])
                validate_positive_bytes(number)

            if unit not in units:
                raise InputException(
                    f'({arg_name}) Invalid byte value: {unit}')
            else:
                return number * units[unit]

    def __init__(self, retry_count, pause_time, max_imgs, with_prompt, api_key, verbose, sorter, limit_rate):
        self.session = requests.Session()

        if verbose != None:
            if not isinstance(verbose, bool):
                raise InputException(
                    'Argument "verbose" provided is not a boolean.')
            self.verbose = verbose
            set_verbose(self.verbose)

        if retry_count != None:
            if not isinstance(retry_count, int) or retry_count < 0:
                raise InputException(
                    'Argument "retry_count" provided is either not an integer or below 0.')
            else:
                self.retry_count = retry_count

        if pause_time != None:
            if not isinstance(pause_time, int) or pause_time < 1:
                raise InputException(
                    'Argument "pause_time" provided is either not an integer or below 1.')
            else:
                self.pause_time = pause_time

        if max_imgs != None:
            if not isinstance(max_imgs, int) or max_imgs < 0:
                raise InputException(
                    'Argument "max_imgs" provided is either not an integer or below 0.')
            else:
                self.max_imgs = max_imgs
        if with_prompt != None:
            if not isinstance(with_prompt, bool):
                raise InputException(
                    'Argument "with_prompt" provided is not a boolean.')
            else:
                self.with_prompt = with_prompt
        if api_key != None:
            if not isinstance(api_key, str) and api_key != None:
                raise InputException(
                    f'Argument "api_key" provided is not a string.')
            else:
                self.api_key = api_key

        if sorter != None:
            if not isinstance(sorter, str):
                raise InputException(
                    'Argument "sorter" provided is not a string.')
            else:
                self.sorter = self.__get_sorter(sorter)

        if limit_rate != None:
            if not (isinstance(limit_rate, str, int, float)):
                raise InputException(
                    'Argument "limit_rate" provided is a string, int or float.')
            else:
                self.limit_rate = self.__parse_bytes(limit_rate, "limit_rate")
