from typing import Dict
import os

# See custom/model_dict-example.json and custom/version_dict-example.json for examples of the kind of data model_dict and version_dict parameters provide.
# Load filter_model by calling the program with --custom-filter=./custom/example.py (or relative to whatever directory you are in currently).


def filter_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This example will filter models based on alphabetical order. There are going to be five directories: A-F, G-L, M-R, S-Z, unidentified"""
    dirs = [('A', 'F'), ('G', 'L'), ('M', 'R'), ('S', 'Z')]
    chosen = 'unidentified'

    for (lowerbound, upperbound) in dirs:
        char = filename[0].upper()
        if lowerbound <= char <= upperbound:
            chosen = lowerbound + '-' + upperbound

    # Here you specify the full path of the directory (minus the parent directory) you want the model to be in
    path = os.path.join(root_path, chosen)  # Example: /A-F
    # Here you specify the name and path of the parent directory that is going to be used to store the model, json and images
    # Example, for figma lora, parent directory path would be /A-F/figma and the safetensors model path would be /A-F/figma/figma.safetensors
    path = os.path.join(path, filename)
    return path
