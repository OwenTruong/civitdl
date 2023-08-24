import sys
import functools

from lib.get_model import download_model

# Have python scan for import-ables
from custom.tags import create_dir_path_by_tag


def format_model(src_dir_path, dst_dir_path):
    None


args_format = ['<Root path of destination directory>', '<model_id>']

if (sys.argv[1] == None or sys.argv[2] == None):
    print(
        f'Error: Missing arguments. Arguments are the following: {args_format}')

download_model(functools.partial(create_dir_path_by_tag,
               root_path=sys.argv[1]), model_id=sys.argv[2])
