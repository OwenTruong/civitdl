
import argparse
import os


from civitconfig.data.configmanager import ConfigManager
from helpers.argparse import PwdAction, ColoredArgParser
from helpers.utils import get_version


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

parser.add_argument('-k', '--api-key', action=PwdAction, type=str, required=False,
                    help='Prompt user for api key to download models that require users to log in.')

parser.add_argument(
    '--with-prompt', action=argparse.BooleanOptionalAction, help='Download images with prompt.'
)

parser.add_argument(
    '--limit-rate', metavar='BYTE', type=str, help='Limit the download speed/rate of resources downloaded from CivitAI.'
)

parser.add_argument(
    '--retry-count', metavar='INT', type=int, help='Specify max number of times to retry downloading a model if it fails.'
)

parser.add_argument(
    '--pause-time', metavar='FLOAT', type=float, help='Specify the number of seconds to pause between each model\'s download.'
)

parser.add_argument(
    '--cache-mode', metavar='MODE', type=str, help='Specify the cache mode. 0 to not use cache. 1 to use cache and copy existant models based on file path. 2 to use cache and copy existant models based on file path + hashes of model. Note that mode 2 has not been implemented yet. See documentation on github for more info.'
)

parser.add_argument(
    '--model-overwrite', action=argparse.BooleanOptionalAction, help='Determine whether to overwrite or skip model download if model is already in path. model=overwrite to overwrite model. no-model-overwrite to skip model.'
)


parser.add_argument(
    '--verbose', action=argparse.BooleanOptionalAction, help='Prints out traceback and other useful information.'
)

parser.add_argument(
    '-v', '--version', action='version', version=f'civitdl v{get_version()}', help='Prints out the version of the program.'
)


def get_args():
    parser_result = parser.parse_args()
    config_manager = ConfigManager()
    config_defaults = config_manager.getDefault()
    sorters = config_manager.getSortersList()
    aliases = config_manager.getAliasesList()

    return {
        "source_strings": parser_result.srcmodels,
        "rootdir": parse_rootdir(aliases, parser_result.rootdir),

        "sorter": parse_sorter(sorters, parser_result.sorter or config_defaults.get('sorter', None)),
        "max_images": parser_result.max_images or config_defaults.get('max_images', None),
        "api_key": parser_result.api_key or config_defaults.get('api_key', None),

        "with_prompt": parser_result.with_prompt or config_defaults.get('with_prompt', None),
        "limit_rate": parser_result.limit_rate or config_defaults.get('limit_rate', None),
        "retry_count": parser_result.retry_count or config_defaults.get('retry_count', None),
        "pause_time": parser_result.pause_time or config_defaults.get('pause_time', None),

        "cache_mode": parser_result.cache_mode or config_defaults.get('cache_mode', None),
        "model_overwrite": parser_result.model_overwrite or config_defaults.get('model_overwrite', None),

        "verbose": False if parser_result.verbose == None else parser_result.verbose
    }
