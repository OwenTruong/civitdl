from typing import Dict
import os


def filter_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """Create nested directories with info about the specific model given root path and the model dict. If no tag is found in the model's json, the default dir path name used will be the last element of twodim_tags' inner list."""
    twodim_tags = [
        ['anime', 'non-anime'],
        ['style', 'poses', 'clothings', 'character',
         'celebrity', 'concept', 'unknown']
    ]

    model_tags = model_dict['tags']
    path = os.path.join(root_path, version_dict['baseModel'].replace(' ', '_'))

    for tags in twodim_tags:
        matched_tags = list(set(tags) & set(model_tags))
        path = os.path.join(
            path, tags[-1] if len(matched_tags) == 0 else matched_tags[0])

    path = os.path.join(path, filename)

    return path
