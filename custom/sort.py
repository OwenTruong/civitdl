from typing import Dict
import os

from civitdl.api.sorter import SorterData, DirName

# See custom/model_dict-example.json and custom/version_dict-example.json for examples of the kind of data model_dict and version_dict parameters provide.


def sort_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This example will sort models based on alphabetical order. There are going to be five directories: A-F, G-L, M-R, S-Z, unidentified"""
    dirs = [('A', 'F'), ('G', 'L'), ('M', 'R'), ('S', 'Z')]
    chosen = 'unidentified'

    for (lowerbound, upperbound) in dirs:
        char = filename[0].upper()
        if lowerbound <= char <= upperbound:
            chosen = lowerbound + '-' + upperbound

    # Here you specify the full path of the directory (minus the parent directory) you want the model to be in
    sub_dir = os.path.join(root_path, chosen)  # Example: /A-F
    # Here you specify the names and paths of the parent directory that is going to be used to store the model, json and images

    model_dir_name = DirName.replace_with_rule_1(model_dict['name'])
    model_dir_path = os.path.join(sub_dir, model_dir_name)
    extra_data_dir_path = os.path.join(
        model_dir_path, f'extra_data-vid_{version_dict["id"]}')

    return SorterData(
        model_dir_path=model_dir_path,
        metadata_dir_path=extra_data_dir_path,
        image_dir_path=extra_data_dir_path,
        prompt_dir_path=extra_data_dir_path
    )
