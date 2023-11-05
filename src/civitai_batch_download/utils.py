import json
from typing import Callable


def write_to_file(path, content, mode: str = None):
    f = open(path, mode) if mode != None else open(path, 'w')
    f.write(content)
    f.close()


def find_in_list(li, cond_fn: Callable[[any, int], bool], default=None):
    """Given a list and a condition function, where the first argument is the index of the item and the second argument is the value of the item, it returns the first value in the list when the condition is true"""
    return next((item for i, item in enumerate(list) if cond_fn(item, int)), default)


def parse_args(args: list[str]):
    """Returns a tuple of (kwargs, args)"""
    kwargs = {}
    non_kwargs = []

    for arg in args:
        if arg.startswith('--'):
            key_value = arg[2:].split('=')
            if len(key_value) == 2:
                key, value = key_value
                kwargs[key] = value
        else:
            non_kwargs.append(arg)

    return (kwargs, non_kwargs)


def err_if_true(condition: bool, message: str, status: int):
    """Raises an exception fi condition is true"""

    if condition:
        dic = {
            "status": status,
            "message": message
        }
        raise Exception(json.dumps(dic))
    else:
        return False


def err_400_if_true(condition: bool, message: str):
    return err_if_true(condition, message, 400)


def err_404_if_true(condition: bool, message: str):
    return err_if_true(condition, message, 404)


def err_500_if_true(condition: bool, message: str):
    return err_if_true(condition, 'InternalError: ' + message, 500)


def err_501_if_true(condition: bool, message: str):
    return err_if_true(condition, 'ImplementationError: ' + message, 501)
