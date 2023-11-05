import os
import time
import re

from .get_model import download_model
from .filters import choose_filter_helper
from .utils import err_400_if_true, err_404_if_true, err_500_if_true, parse_args


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


def get_model_ids(type: str, source: str):
    """Type can be any of the actions"""
    ids = source

    # TODO: make it so we don't have to guess types

    if type == 'batchfile':
        with open(source, 'r') as file:
            ids = file.read().strip()
    ids = ids.split(',')
    ids = [re.findall(r'\d+', id) for id in ids]
    ids = [id for id in ids if len(id) > 0]
    print(ids)
    return ids


def batch_download(type: str, argv: list[str]):
    """Accepted type are batchfile and batchstr"""
    message = args_message[type]
    kwargs, args = parse_args(argv)
    err_400_if_true(len(args) < 2,
                    f'Missing arguments. Arguments are the following: {message["args_format"]}.\nExample: {message["example"]}')
    err_404_if_true(type != 'batchstr' and not os.path.exists(
        args[0]), 'Source directory does not exist.')

    ids = None
    if type == 'batchfile':
        ids = get_model_ids(type, args[0])
    elif type == 'batchstr':
        ids = get_model_ids(type, args[0])
    else:
        err_500_if_true(True, ValueError,
                        f'Unknown batch type --> {type}')

    err_500_if_true(ids == None, 'ids is of type None')

    filter_model = choose_filter_helper(kwargs)
    err_500_if_true(filter_model == None,
                    'Error: filter_model is of type None')

    for id in ids:
        model_id = id[0]
        version_id = id[1] if len(id) == 2 else None
        download_model(model_id=model_id, create_dir_path=filter_model,
                       dst_root_path=args[1], max_img_count=(kwargs['max-images'] if 'max-images' in kwargs else 3), version_id=version_id)
        time.sleep(2)
