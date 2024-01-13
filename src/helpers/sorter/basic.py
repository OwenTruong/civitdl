from typing import Dict
import os

from civitdl.sorter_api import Validation, SorterConfig


def sort_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This is useful when you only just want all of the lora/checkpoint/etc. in the same root directory. Metadata + images are downloaded inside a directory under the parent directory."""
    parent_dir_name = model_dict['name']
    parent_dir_path = os.path.join(root_path, parent_dir_name)
    extra_data_dir_path = os.path.join(
        parent_dir_path, f'extra_data-vid_{version_dict["id"]}')

    return SorterConfig(
        parent_dir_name,
        parent_dir_path,
        metadata_dir_path=extra_data_dir_path,
        image_dir_path=extra_data_dir_path,
        prompt_dir_path=extra_data_dir_path
    )
