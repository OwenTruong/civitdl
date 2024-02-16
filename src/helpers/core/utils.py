from datetime import datetime
import sys
import importlib.metadata
from typing import Callable
import concurrent.futures
from tqdm import tqdm

from ._ui.styler import Styler, disable_style, CustomException, InputException, ResourcesException, UnexpectedException, APIException, NotImplementedException
from ._validation import Validation

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
    return now.strftime("%Y_%m_%d-%Hm_%Mm_%Ss_%f")


def get_version():
    return importlib.metadata.version('civitdl')


def sprint(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except:
        encoded_args = [str(arg).encode(
            'utf-8', 'replace') for arg in args]
        print(*encoded_args, **kwargs)


# Level 1 - Currently or in the future might depends on level 0


def run_verbose(fn, *args, **kwargs):
    if get_verbose():
        fn(*args, **kwargs)


def print_verbose(*args, **kwargs):
    if get_verbose():
        args = [Styler.stylize(str(arg), bg_color='info') for arg in args]
        sprint(*args, **kwargs)


def print_exc(exc: Exception, *args, **kwargs):
    if isinstance(exc, CustomException):
        sprint(exc, file=sys.stderr, *args, **kwargs)
    else:
        sprint(Styler.stylize(str(exc), color='exception'), *args,
               file=sys.stderr, **kwargs)


def print_newlines(string: str, **kwargs):
    for el in string.split('\n'):
        sprint(el, **kwargs)


def print_error(*args, **kwargs):
    args = [Styler.stylize(str(arg), bg_color='error') for arg in args]
    sprint(*args, **kwargs, file=sys.stderr)


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
                unit='iB', unit_scale=True, file=sys.stdout)


def find_in_list(li, cond_fn: Callable[[any, int], bool], default=None):
    """Given a list and a condition function, where the first argument is the index of the item and the second argument is the value of the item, it returns the first value in the list when the condition is true"""
    return next((item for i, item in enumerate(li) if cond_fn(item, int)), default)
