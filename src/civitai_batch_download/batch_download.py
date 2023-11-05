import ast
import os
import time
from traceback import print_exc
from termcolor import colored

from .get_model import download_model
from .filters import choose_filter_helper
from .utils import err_400_if_true, err_404_if_true, err_500_if_true, err_501_if_true, err_if_true, parse_args


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
    string = source
    if type == 'batchfile':
        with open(source, 'r') as file:
            string = file.read().strip()
    res = [input_str for input_str in string.replace(
        '\n', '').split(',') if input_str.strip() != '']
    return res


def batch_download(type: str, argv: list[str]):
    """Accepted type are batchfile and batchstr"""
    err_500_if_true(type != 'batchfile' and type != 'batchstr',
                    f'Unknown batch type --> {type}')

    message = args_message[type]
    kwargs, args = parse_args(argv)
    err_400_if_true(len(args) < 2,
                    f'Missing arguments. Arguments are the following: {message["args_format"]}.\nExample: {message["example"]}')
    err_404_if_true(type != 'batchstr' and not os.path.exists(
        args[0]), 'Source directory does not exist.')

    input_li = None
    input_li = get_input_strings(type, args[0])

    err_500_if_true(input_li == None, 'input_li is of type None')
    err_500_if_true(len(input_li) == None,
                    f'get_input_strings was not able to parse argument, {args[0]}')

    filter_model = choose_filter_helper(kwargs)
    err_500_if_true(filter_model == None,
                    'Error: filter_model is of type None')

    for input_str in input_li:
        try:
            download_model(
                input_str=input_str,
                create_dir_path=filter_model,
                dst_root_path=args[1],
                download_image=True,
                max_img_count=(kwargs['max-images'] if 'max-images' in kwargs else 3))
            time.sleep(2)
        except Exception as e:
            try:
                res = ast.literal_eval(str(e))
                print(
                    f"{colored('Status ' + str(res['status']), 'red', attrs=['bold'])}: {colored(res['message'], 'red')}")
            except:
                # TODO: What do we do about error status from civitai's server?
                print_exc(e)
