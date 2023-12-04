import os
import time
import traceback
from typing import List


from .get_model import download_model
from .filters import choose_filter_helper
from .utils import parse_args, run_in_dev

from .exceptions import InputException, UnexpectedException

args_message = {
    'batchfile': {
        'args_format': '<Comma Separated File> <Destination Path> --custom-filter=<Path to filter file (optional)> --filter=<tags (optional)> --max-images=<default=3 (optional)',
        'example': '~/lora-to-download.txt ~/organized_loras --custom-filter=example.py'
    },
    'batchstr': {
        'args_format': '<Comma Separated File> <Destination Path> --custom-filter=<Path to filter file (optional)> --filter=<tags (optional)> --max-images=<default=3 (optional)',
        'example': '"123456,78901,23456" ~/organized_loras --custom-filter=example.py'
    }
}


def get_input_strings(type: str, source: str):
    if len(source.strip()) == 0:
        raise InputException('No model id or url provided')
    string = source
    if type == 'batchfile':
        with open(source, 'r') as file:
            string = file.read().strip()
    res = [input_str for input_str in string.replace(
        '\n', '').split(',') if input_str.strip() != '']
    return res


# TODO: Add error checking for the kwargs

def verify_custom_filter():
    None


def verify_filter():
    None


def verify_max_images():
    None


def batch_download(type: str, argv: List[str]):
    """Accepted type are batchfile and batchstr"""
    if type != 'batchfile' and type != 'batchstr':
        raise UnexpectedException(f'Unknown batch type --> {type}')

    message = args_message[type]
    kwargs, args = parse_args(argv)
    input_li = None
    filter_model = None

    if len(args) < 2:
        raise InputException(
            'Missing arguments.',
            f'Arguments should be in the following format: {message["args_format"]}.', f'Example: {message["example"]}'
        )
    elif type == 'batchfile' and not os.path.exists(args[0]):
        raise InputException(f'Batch file does not exist at path: {args[0]}')

    input_li = get_input_strings(type, args[0])

    if input_li == None:
        raise UnexpectedException('input_li is of type None')
    elif len(input_li) == 0:
        raise InputException(
            f'get_input_strings was not able to parse argument: {args[0]}')

    filter_model = choose_filter_helper(kwargs)

    if (filter_model == None):
        raise UnexpectedException('filter_model is of type None')

    for input_str in input_li:
        try:
            download_model(
                input_str=input_str,
                create_dir_path=filter_model,
                dst_root_path=args[1],
                download_image=True,
                max_img_count=(kwargs['max-images'] if 'max-images' in kwargs else 3))
            time.sleep(3)
        except Exception as e:
            print('---------')
            run_in_dev(traceback.print_exc)
            print(e)
            print('---------')
