from typing import Dict
import os

from civitdl.api.sorter import SorterData, DirName


def sort_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """Create nested directories with info about the specific model given root path and the model dict. If no tag is found in the model's json, the default dir path name used will be 'others'."""
    twodim_tags = [
        ['anime', 'others'],
        ['style', 'poses', 'clothings', 'character',
         'celebrity', 'concept', 'others']
    ]

    model_tags = model_dict['tags']
    path = os.path.join(root_path, version_dict['baseModel'].replace(' ', '_'))

    for tags in twodim_tags:
        matched_tags = list(set(tags) & set(model_tags))
        path = os.path.join(
            path, tags[-1] if len(matched_tags) == 0 else matched_tags[0])

    model_dir_name = DirName.replace_with_rule_1(model_dict['name'])
    model_dir_path = os.path.join(path, model_dir_name)
    extra_data_dir_path = os.path.join(
        model_dir_path, f'extra_data-vid_{version_dict["id"]}')

    return SorterData(
        model_dir_path=model_dir_path,
        metadata_dir_path=extra_data_dir_path,
        image_dir_path=extra_data_dir_path,
        prompt_dir_path=extra_data_dir_path
    )
