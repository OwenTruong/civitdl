import sys
import functools

from lib.get_lora_api import download_model
from custom.tags import create_dir_path_by_tag

# download_model(dst_dir_path='manuel-test',
#                model_id=sys.argv[1], version_id=115273)


def format_model(src_dir_path, dst_dir_path):
    None


args_format = ['<Root path of destination directory>', '<model_id>']

if (sys.argv[1] == None or sys.argv[2] == None):
    print(
        f'Error: Missing arguments. Arguments are the following: {args_format}')

download_model(functools.partial(create_dir_path_by_tag,
               root_path=sys.argv[1]), model_id=sys.argv[2])
