from typing import Callable


def write_to_file(path, content, mode: str = None):
    f = open(path, mode) if mode != None else open(path, 'w')
    f.write(content)
    f.close()


def find_in_list(li, cond_fn: Callable[[any, int], bool], default=None):
    """Given a list and a condition function, where the first argument is the index of the item and the second argument is the value of the item, it returns the first value in the list when the condition is true"""
    return next((item for i, item in enumerate(list) if cond_fn(item, int)), default)
