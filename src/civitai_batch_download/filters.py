import importlib.util
from typing import Dict
import os


def create_basic_path(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This is useful when you only just want all of the lora in the same parent folder."""
    return os.path.join(root_path, filename)


def create_path_by_tags(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
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


def choose_filter_helper(kwargs: Dict[str, str]):
    filter_model = None
    if 'custom-filter' in kwargs:
        if not os.path.exists(kwargs['custom-filter']):
            return print('Error: Custom filter python file does not exist')
        spec = importlib.util.spec_from_file_location(
            'plugin', kwargs['custom-filter'])
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)
        filter_model = plugin.filter_model
    elif 'filter' in kwargs:
        if kwargs['filter'] == 'tags':
            filter_model = create_path_by_tags
        elif kwargs['filter'] == 'basic':
            filter_model = create_basic_path
        else:
            return print(f'Error: Unknown filter specified. The available built-in filters are {["tags", "basic"]} (basic is the default filter)')
    else:
        filter_model = create_basic_path
    return filter_model
