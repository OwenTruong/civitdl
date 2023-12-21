from typing import Dict
import os

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

    parent_dir = os.path.join(sub_dir, model_dict['name'])
    extra_data_dir = os.path.join(
        parent_dir, f'extra_data-vid_{version_dict["id"]}')
    paths = [
        parent_dir,      # model dir path
        extra_data_dir,  # metadata dir path
        extra_data_dir,  # image dir path
        extra_data_dir   # prompt dir path
    ]
    return paths
