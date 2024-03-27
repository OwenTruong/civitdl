from typing import Callable, Dict, List, Literal, Union, Optional
import requests

from helpers.sorter.utils import SorterData, import_sort_model
from helpers.sorter import basic, tags
from helpers.core.utils import disable_style, InputException, NotImplementedException, UnexpectedException, Validation, print_verbose, safe_run, set_verbose


def parse_bytes(size: Union[str, int, float], name: str):
    units = {"k": 10**3, "m": 10**6, "g": 10**9, "t": 10**12}

    res = safe_run(float, size)
    if res["success"] == True:
        number = round(res["data"])
        Validation.validate_integer(number, name)
        return number
    else:
        number, unit = (size[0:-1], size[-1:].lower())

        num_res = safe_run(float, number)
        if num_res["success"] == False:
            raise InputException(
                f'Invalid byte value for {name}: {size}')
        else:
            number = round(num_res["data"])
            Validation.validate_integer(number, name)

        if unit not in units:
            raise InputException(
                f'Invalid byte value for {name}: {unit}')
        else:
            return number * units[unit]


class BatchOptions:
    sorter_name: str
    sorter: Callable[[Dict, Dict, str, str],
                     SorterData] = basic.sort_model
    max_images: int = 3
    nsfw_mode: Literal['0', '1', '2'] = '1'
    api_key: Optional[str] = None

    with_prompt: bool = True
    without_model: bool = False
    limit_rate: int = 0
    retry_count: int = 3
    pause_time: int = 3

    cache_mode: Literal['0', '1', '2'] = '1'
    model_overwrite: bool = False

    with_color: bool = False
    verbose: Optional[bool] = None

    def __get_sorter(self, sorter: str):
        if not isinstance(sorter, property) and not isinstance(sorter, str):
            raise InputException(
                'Sorter provided is not a string in BatchOptions.')

        sorter_str = 'basic' if isinstance(sorter, property) else sorter
        if sorter_str == 'basic' or sorter_str == 'tags':
            self._sorter = tags.sort_model if sorter_str == 'tags' else basic.sort_model
        else:
            self._sorter = import_sort_model(sorter_str)

        print_verbose("Chosen Sorter Description: ", self._sorter.__doc__)
        return self._sorter

    def __init__(self, retry_count, pause_time, max_images, nsfw_mode, with_prompt, without_model, api_key, verbose, sorter, limit_rate, cache_mode, model_overwrite, with_color):
        self.session = requests.Session()

        # FIXME: Move usage of with_color and verbose outside of options
        if with_color is not None:
            Validation.validate_bool(with_color, 'with_color')
            self.with_color = with_color
            if with_color == False:
                disable_style()

        if verbose is not None:
            Validation.validate_bool(verbose, 'verbose')
            self.verbose = verbose
            if verbose == True:
                set_verbose(self.verbose)

        if sorter is not None:
            Validation.validate_string(sorter, 'sorter')
            self.sorter = self.__get_sorter(sorter)
            self.sorter_name = sorter

        if max_images is not None:
            Validation.validate_integer(max_images, 'max_images', min_value=0)
            self.max_images = max_images

        if nsfw_mode is not None:
            Validation.validate_string(
                nsfw_mode, 'nsfw_mode', whitelist=['0', '1', '2'])
            self.nsfw_mode = nsfw_mode

        if api_key is not None and api_key != '':
            Validation.validate_string(api_key, 'api_key')
            self.api_key = api_key

        if with_prompt is not None:
            Validation.validate_bool(with_prompt, 'with_prompt')
            self.with_prompt = with_prompt

        if without_model is not None:
            Validation.validate_bool(without_model, 'without_model')
            self.without_model = without_model

        if limit_rate is not None:
            Validation.validate_types(
                limit_rate, [str, int, float], 'limit_rate')
            self.limit_rate = parse_bytes(limit_rate, "limit_rate")

        if retry_count is not None:
            Validation.validate_integer(
                retry_count, 'retry_count', min_value=0)
            self.retry_count = retry_count

        if pause_time is not None:
            Validation.validate_float(pause_time, 'pause_time', min_value=0)
            self.pause_time = pause_time

        if cache_mode is not None:
            Validation.validate_string(
                cache_mode, 'cache_mode', whitelist=['0', '1', '2'])
            if cache_mode == '2':
                raise NotImplementedException(
                    'cache mode of 2 has not been implemented yet')
            self.cache_mode = cache_mode

        if model_overwrite is not None:
            Validation.validate_bool(model_overwrite, 'model_overwrite')
            self.model_overwrite = model_overwrite


class DefaultOptions:
    sorter: Optional[str] = None
    max_images: Optional[int] = None
    nsfw_mode: Optional[int] = None
    api_key: Optional[str] = None

    with_prompt: Optional[bool] = None
    without_model: Optional[bool] = None
    limit_rate: Optional[str] = None
    retry_count: Optional[int] = None
    pause_time: Optional[int] = None

    cache_mode: Optional[int] = None
    model_overwrite: Optional[bool] = None

    with_color: Optional[bool] = None

    def __init__(self, sorter=None, max_images=None, nsfw_mode=None, api_key=None, with_prompt=None, without_model=None, limit_rate=None, retry_count=None, pause_time=None, cache_mode=None, model_overwrite=None, with_color=None):
        if sorter is not None:
            Validation.validate_string(
                sorter, 'sorter')

            self.sorter = sorter

        if max_images is not None:
            Validation.validate_integer(
                max_images, 'max_images', min_value=0
            )
            self.max_images = max_images

        if nsfw_mode is not None:
            Validation.validate_string(
                nsfw_mode, 'nsfw_mode', whitelist=['0', '1', '2']
            )
            self.nsfw_mode = nsfw_mode

        if api_key is not None:
            Validation.validate_string(api_key, 'api_key')
            self.api_key = api_key

        if with_prompt is not None:
            Validation.validate_bool(with_prompt, 'with_prompt')
            self.with_prompt = with_prompt

        if without_model is not None:
            Validation.validate_bool(without_model, 'without_model')
            self.without_model = without_model

        if limit_rate is not None:
            Validation.validate_string(limit_rate, 'limit_rate')
            parse_bytes(limit_rate, 'limit_rate')
            self.limit_rate = limit_rate

        if retry_count is not None:
            Validation.validate_integer(
                retry_count, 'retry_count', min_value=0
            )
            self.retry_count = retry_count

        if pause_time is not None:
            Validation.validate_float(
                pause_time, 'pause_time', min_value=0
            )
            self.pause_time = pause_time

        if cache_mode is not None:
            Validation.validate_string(
                cache_mode, 'cache_mode', whitelist=['0', '1', '2']
            )
            if cache_mode == '2':
                raise NotImplementedException(
                    'cache mode of 2 has not been implemented yet')
            self.cache_mode = cache_mode

        if model_overwrite is not None:
            Validation.validate_bool(model_overwrite, 'model_overwrite')
            self.model_overwrite = model_overwrite

        if with_color is not None:
            Validation.validate_bool(with_color, 'with_color')
            self.with_color = with_color
