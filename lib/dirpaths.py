from typing import Dict
import os


def create_basic_path(metadata: Dict, model_data: Dict, filename: str, root_path: str):
    """ This is useful when you only just want all of the lora in the same parent folder."""
    return os.path.join(root_path, filename)


def create_path_by_tags(metadata: Dict, model_data: Dict, filename: str, root_path: str):
    """Create nested directories with info about the specific model given root path and the model dict. If no tag is found in the model's json, the default dir path name used will be the last element of twodim_tags' inner list."""
    twodim_tags = [
        ['anime', 'non-anime'],
        ['style', 'character',
         'celebrity', 'clothings', 'poses', 'concept', 'unknown']
    ]

    model_tags = metadata['tags']
    path = os.path.join(root_path, model_data['baseModel'].replace(' ', '_'))

    for tags in twodim_tags:
        matched_tags = list(set(tags) & set(model_tags))
        path = os.path.join(
            path, tags[-1] if len(matched_tags) == 0 else matched_tags[0])

    path = os.path.join(path, filename)

    return path
