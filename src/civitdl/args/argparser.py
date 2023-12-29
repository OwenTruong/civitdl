import argparse
import os


from civitconfig.data.configmanager import ConfigManager
from helpers.argparse import PwdAction, ColoredArgParser


def parse_sorter(sorters, sorter_str):
    for sorter in sorters:
        if sorter_str == sorter[0]:
            return sorter[2]

    return sorter_str


def parse_rootdir(aliases, path):
    dirs = path.split(os.path.sep)

    for alias in aliases:
        if alias[0] == dirs[0]:
            newpath = os.path.join(alias[1], *dirs[1:])
            return parse_rootdir(aliases, newpath)

    return path


HELP_MESSAGE_FOR_SRC_MODEL = """
Provide one or more sources as arguments.
A source can be one of the following: model ID, CivitAI URL, string list of sources or batchfiles.
- batchfiles must be a textfile of comma separated list of sources.
- string list of sources in the following example is "sourceA, sourceB, sourceC, ...":
- Example 1: civitdl source1 "sourceA, sourceB, sourceC, ..." source2 ./path/to/root/model/directory
- Example 2: civitdl ./batchfile1.txt 123456 ~/Downloads/ComfyUI/models/loras
"""

parser = ColoredArgParser(
    prog='civitdl',
    description="A CLI python script to batch download models from CivitAI with CivitAI Api V1.",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('srcmodels', type=str, action="extend", nargs='+',
                    help=HELP_MESSAGE_FOR_SRC_MODEL)
parser.add_argument('rootdir', type=str,
                    help='Root directory of where the downloaded model should go.')
parser.add_argument('-s', '--sorter', type=str,
                    help='Specify which sorter function to use.\nDefault is "basic" sorter.\nProvide file path to sorter function if you wish to use a custom sorter.')
parser.add_argument('-i', '--max-images', metavar='INT', type=int,
                    help='Specify max images to download for each model.')

parser.add_argument('-p', '--with-prompt', action=argparse.BooleanOptionalAction,
                    help='Download images with prompt.')

parser.add_argument('-k', '--api-key', action=PwdAction, type=str, nargs=0,
                    help='Prompt user for api key to download models that require users to log in.')

parser.add_argument(
    '-v', '--verbose', action=argparse.BooleanOptionalAction, help='Prints out traceback and other useful information.')


def get_args():
    parser_result = parser.parse_args()
    config_manager = ConfigManager()
    d_max_imgs, d_with_prompt, d_sorter_name, d_api_key = config_manager.getDefaultAsList()
    sorters = config_manager.getSortersList()
    aliases = config_manager.getAliasesList()

    return {
        "source_strings": parser_result.srcmodels,
        "rootdir": parse_rootdir(aliases, parser_result.rootdir),
        "sorter": parse_sorter(sorters, parser_result.sorter or d_sorter_name),
        "max_imgs": parser_result.max_images or d_max_imgs,
        "with_prompt": parser_result.with_prompt or d_with_prompt,
        "api_key": parser_result.api_key or d_api_key,
        "verbose": False if parser_result.verbose == None else parser_result.verbose
    }
