from typing import Dict
import os

from civitdl.api.sorter import SorterData, DirName


def sort_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This is useful when you only just want all of the lora/checkpoint/etc. in the same root directory. Metadata + images are downloaded inside a directory under the parent directory."""
    model_dir_name = DirName.replace_with_rule_1(model_dict['name'])
    model_dir_path = os.path.join(root_path, model_dir_name)
    extra_data_dir_path = os.path.join(
        model_dir_path, f'extra_data-vid_{version_dict["id"]}')

    return SorterData(
        model_dir_path=model_dir_path,
        metadata_dir_path=extra_data_dir_path,
        image_dir_path=extra_data_dir_path,
        prompt_dir_path=extra_data_dir_path
    )
