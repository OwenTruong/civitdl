import os
import re
from typing import List, Union

import argparse
from termcolor import colored

from civitconfig.data.configmanager import ConfigManager
from helpers.utils import set_env
from helpers.argparse import PwdAction
from helpers.exceptions import InputException, UnexpectedException

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


def use_parent_dir_if_exist(src: str, parent: Union[str, None]) -> str:
    return os.path.join(os.path.dirname(parent), src) if parent else src


def parse_src(str_li: List[str], parent: Union[str, None] = None):
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
        elif os.path.exists(use_parent_dir_if_exist(string, parent)):
            string = use_parent_dir_if_exist(string, parent)
            file_str = None

            with open(string, 'r') as file:
                file_str = file.read().strip()
            if file_str == None:
                raise UnexpectedException(
                    'Unknown exception while reading batchfile path.')
            str_li_res = get_comma_list(file_str)
            res.extend(parse_src(str_li_res, parent=string))
        else:
            print(colored(f'Bad source provided: {string}', 'red'))

    return res


def parse_rootdir(aliases, path):
    dirs = path.split(os.path.sep)

    for alias in aliases:
        if alias[0] == dirs[0]:
            newpath = os.path.join(alias[1], *dirs[1:])
            return parse_rootdir(aliases, newpath)

    return path


def parse_sorter(sorters, sorter_str):
    for sorter in sorters:
        if sorter_str == sorter[0]:
            return sorter[2]

    return sorter_str


HELP_MESSAGE_FOR_SRC_MODEL = """
Provide one or more sources as arguments.
A source can be one of the following: model ID, CivitAI URL, string list of sources or batchfiles.
- batchfiles must be a textfile of comma separated list of sources.
- string list of sources in the following example is "sourceA, sourceB, sourceC, ...":
- Example 1: civitdl source1 "sourceA, sourceB, sourceC, ..." source2 ./path/to/root/model/directory
- Example 2: civitdl ./batchfile1.txt 123456 ~/Downloads/ComfyUI/models/loras
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
parser.add_argument('-s', '--sorter', type=str,
                    help='Specify which sorter function to use.\nDefault is "basic" sorter.\nProvide file path to sorter function if you wish to use a custom sorter.')
parser.add_argument('-i', '--max-images', metavar='INT', type=int,
                    help='Specify max images to download for each model.')

parser.add_argument('-p', '--with-prompt', action=argparse.BooleanOptionalAction, help='Download images with prompt.')

parser.add_argument('-k', '--api-key', action=PwdAction, type=str, nargs=0,
                    help='Prompt user for api key to download models that require users to log in.')

parser.add_argument(
    '-v', '--dev', action=argparse.BooleanOptionalAction, help='Prints out traceback and other useful information.')


def get_args():
    parser_result = parser.parse_args()
    config_manager = ConfigManager()
    d_max_imgs, d_with_prompt, d_sorter_name, d_api_key = config_manager.getDefaultAsList()
    sorters = config_manager.getSortersList()
    aliases = config_manager.getAliasesList()

    if parser_result.dev:
        set_env('development')

    return {
        "ids": parse_src(parser_result.srcmodel),
        "rootdir": parse_rootdir(aliases, parser_result.rootdir),
        "sorter": parse_sorter(sorters, parser_result.sorter or d_sorter_name),
        "max_imgs": parser_result.max_images or d_max_imgs,
        "with_prompt": parser_result.with_prompt or d_with_prompt,
        "api_key": parser_result.api_key or d_api_key
    }
