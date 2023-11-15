import os
import re
from typing import List

import argparse

from termcolor import colored

from ..helper.exceptions import InputException, UnexpectedException

__all__ = ['Id', 'get_args']


class Id:
    def __init__(self, type, data: List[str], original: str):
        if type != 'id' and type != 'site' and type != 'api':
            raise UnexpectedException(
                f'Unknown type provided for Id class: {type}')

        for el in data:
            if not isinstance(el, str):
                raise UnexpectedException(
                    f'Wrong data type for {el} in {data}')

        if not isinstance(original, str):
            raise UnexpectedException(f'Wrong data type for {original}')

        self.type = type
        self.data = data
        self.original = original


def get_comma_list(string: str) -> List[str]:
    return [input_str for input_str in string.replace(
        '\n', '').split(',') if input_str.strip() != '']


def parse_src(str_li: List[str], parent=None):
    res: List[Id] = []
    for string in str_li:
        string = string.strip()

        if string.isdigit() and abs(int(string)) == int(string):
            res.append(Id('id', [string], string))
        elif len(get_comma_list(string)) > 1:
            arg_str_li = get_comma_list(string)
            res.extend(parse_src(arg_str_li))
        elif 'civitai.com/api' in string:
            version_id_regex = r'(?<=models\/)\d+'
            version_id = re.search(version_id_regex, string)
            if version_id == None:
                err = 'Incorrect format for the url provided' + \
                    (f' in {parent}: ' if parent else ': ') + string
                raise InputException(err)
            version_id = version_id.group(0)
            res.append(Id('api', [version_id], string))
        elif 'civitai.com/models' in string:
            model_id = re.search(r'(?<=models\/)\d+', string)
            version_id = re.search(r'(?<=modelVersionId=)\d+', string)

            if model_id == None:
                err = 'Incorrect format for the url/id provided' + \
                    (f' in {parent}: ' if parent else ': ') + string
                raise InputException(err)
            model_id = model_id.group(0)

            if version_id:
                version_id = version_id.group(0)
                res.append(
                    Id('site', [model_id, version_id], string))
            else:
                res.append(Id('site', [model_id], string))
        elif os.path.exists(string):
            file_str = None
            with open(string, 'r') as file:
                file_str = file.read().strip()
            str_li_res = get_comma_list(file_str)
            res.extend(parse_src(str_li_res, string))
        else:
            print(colored(f'Bad source provided: {string}', 'red'))

    return res


def parse_sorter(str):
    if os.path.exists(str):
        return {
            "type": 'path',
            "data": str
        }
    elif str == 'basic' or str == 'tags':
        return {
            "type": 'default',
            "data": str
        }
    else:
        raise InputException(f'Sorter does not exist: {str}')


HELP_MESSAGE_FOR_SRC_MODEL = """
Provide one or more elements as arguments.
An element can be one of the following: model ID, CivitAI URL, string list of elements or batchfiles.
- batchfiles must be a textfile of comma separated list of elements.
- string list of elements in the following example is "element2, element3, element4, ...": 
- Example 1: civitdl element1 "element2, element3, element4, ..." element5 ./path/to/root/model/directory
- Example 2 (download some loras): civitdl ./batchfile1.txt 123456 ~/Downloads/ComfyUI/models/loras
"""

parser = argparse.ArgumentParser(
    prog='civitdl',
    description="A CLI python script to batch download models from CivitAI with CivitAI Api V1.",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('srcmodel', type=str, action="extend", nargs='+',
                    help=HELP_MESSAGE_FOR_SRC_MODEL)
parser.add_argument('rootdir', type=str,
                    help='Root directory of where the downloaded model should go.')
parser.add_argument('-s', '--sorter', type=str, default='basic',
                    help='Specify which sorter function to use. Default is "basic" sorter. Provide path to sorter function if you wish to use a specific sorter.')
parser.add_argument('-m', '--max-images', type=int, default=3,
                    help='Specify max images to download for each model.')


def get_args():
    parser_result = parser.parse_args()
    return {
        "ids": parse_src(parser_result.srcmodel),
        "rootdir": parser_result.rootdir,
        "sorter": parse_sorter(parser_result.sorter),
        "max_imgs": parser_result.max_images
    }