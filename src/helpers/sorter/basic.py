from typing import Dict
import os


def sort_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This is useful when you only just want all of the lora/checkpoint/etc. in the same parent folder."""
    return os.path.join(root_path, filename)
