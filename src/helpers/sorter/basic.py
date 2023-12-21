from typing import Dict
import os


def sort_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This is useful when you only just want all of the lora/checkpoint/etc. in the same root directory. Metadata + images are downloaded inside a directory under the parent directory."""
    parent_dir = os.path.join(root_path, model_dict['name'])
    extra_data_dir = os.path.join(
        parent_dir, f'extra_data-vid_{version_dict["id"]}')
    paths = [
        parent_dir,      # model dir path
        extra_data_dir,  # metadata dir path
        extra_data_dir,  # image dir path
        extra_data_dir   # prompt dir path
    ]
    return paths
