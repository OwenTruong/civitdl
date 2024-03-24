from ._ui.styler import Styler, InputException, UnexpectedException
from .constants import BLACKLISTED_DIR_CHARS
import sys
import os
from typing import Iterable, Union


class Validation:
    @staticmethod
    def __validate_arg_name(arg_name):
        if not isinstance(arg_name, str):
            raise UnexpectedException(
                f'Name/title of validator is not a string (arg_name: {arg_name})')

        if len(arg_name) == 0:
            raise UnexpectedException(
                f'Name/title of validator is not defined (arg_name: {arg_name}, length of arg_name: {len(arg_name)})')

    @staticmethod
    def __validate_range(min, max):
        if min is not None and not isinstance(min, (int, float)):
            raise UnexpectedException(
                f'Minimum number provided is not a number (min: {min}, type: {type(min)}).')

        if max is not None and not isinstance(max, (int, float)):
            raise UnexpectedException(
                f'Maximum number provided is not a number (max: {max}, type: {type(max)})')

        if max is not None and min is not None and max < min:
            raise UnexpectedException(
                f'Maximum is smaller than minimum allowed number in range (min: {min}, max: {max})')

    @classmethod
    def validate_string(cls, value, arg_name: str, min_len: Union[int, None] = None, max_len: Union[int, None] = None, whitelist: Iterable[str] = [], blacklist: Iterable[str] = []) -> str:
        # Validate keyword arguments

        cls.__validate_arg_name(arg_name)
        cls.__validate_range(min_len, max_len)
        if min_len is not None and min_len < 0:
            raise UnexpectedException(
                f'Minimum length provided with value "{value}" is below 0 (min_len: {min_len}).')
        if max_len is not None and max_len < 0:
            raise UnexpectedException(
                f'Maximum length provided with value "{value}" is below 0 (max_len: {max_len}).')

        if not isinstance(whitelist, Iterable):
            raise UnexpectedException(
                f'Whitelist provided with value "{value}" is not a list (whitelist: {whitelist}).')
        if not all(isinstance(item, str) for item in whitelist):
            raise UnexpectedException(
                f'Whitelist provided with value "{value}" contains non-string elements (whitelist: {whitelist}).')

        if not isinstance(blacklist, Iterable):
            raise UnexpectedException(
                f'Blacklist provided with value "{value}" is not a list (blacklist: {blacklist}).')
        if not all(isinstance(item, str) for item in blacklist):
            raise UnexpectedException(
                f'Blacklist provided with value "{value}" contains non-string elements (blacklist: {blacklist}).')
        if len(whitelist) > 0 and len(blacklist) > 0:
            raise UnexpectedException(
                f'Both whitelist and blacklist provided with value "{value}" is not empty. You can not have both whitelist and blacklist (whitelist: {whitelist}, blacklist: {blacklist}).')

        # Validate value

        if not isinstance(value, str):
            raise InputException(
                f'Value provided for {arg_name} is not a string (value: {value}, type: {type(value)}).')

        if value == '':
            raise InputException(
                f'Value provided for {arg_name} is empty.')

        if min_len is not None and len(value) < min_len:
            raise InputException(
                f'Value provided for {arg_name} is below minimum length allowed (value: {value}, min_len: {min_len}).')

        if max_len is not None and len(value) > max_len:
            raise InputException(
                f'Value provided for {arg_name} is above maximum length allowed (value: {value}, min_len: {min_len}).')

        if whitelist != [] and value not in whitelist:
            raise InputException(
                f'Value provided for {arg_name} is not in whitelist (value: {value}, whitelist: {whitelist}).')

        if blacklist != [] and value in blacklist:
            raise InputException(
                f'Value provided for {arg_name} is in blacklist (value: {value}, blacklist: {blacklist}).')

        return value

    @classmethod
    def validate_integer(cls, value, arg_name: str, min_value: Union[int, None] = None, max_value: Union[int, None] = None) -> int:
        # validate keyword arguments

        cls.__validate_arg_name(arg_name)
        cls.__validate_range(min_value, max_value)

        # Validate value

        if not isinstance(value, int):
            raise InputException(
                f'Value provided for {arg_name} is not an number (value: {value}, type: {type(value)}).')

        if min_value is not None and value < min_value:
            raise InputException(
                f'Value provided for {arg_name} is below the minimum number allowed (value: {value}, min_value: {min_value})')

        if max_value is not None and value > max_value:
            raise InputException(
                f'Value provided for {arg_name} is above the minimum number allowed (value: {value}, max_value: {max_value})')

        return value

    @classmethod
    def validate_float(cls, value, arg_name: str, min_value: Union[float, None] = None, max_value: Union[float, None] = None) -> float:
        # Validate keyword arguments

        cls.__validate_arg_name(arg_name)
        cls.__validate_range(min_value, max_value)

        # Validate value

        if not isinstance(value, float):
            raise InputException(
                f'Value provided for {arg_name} is not a number (value: {value}, type: {type(value)}).')

        if min_value is not None and value < min_value:
            raise InputException(
                f'Value provided for {arg_name} is below the minimum number allowed (value: {value}, min_value: {min_value})')

        if max_value is not None and value > max_value:
            raise InputException(
                f'Value provided for {arg_name} is above the minimum number allowed (value: {value}, max_value: {max_value})')

        return value

    @classmethod
    def validate_bool(cls, value, arg_name: str) -> bool:
        # Validate keyword arguments

        cls.__validate_arg_name(arg_name)

        # Validate value
        if not isinstance(value, bool):
            raise InputException(
                f'Value provided for {arg_name} is not a bool (value: {value}, type: {type(value)})')
        return value

    @classmethod
    def validate_types(cls, value, types, arg_name: str):
        # Validate keyword arguments

        cls.__validate_arg_name(arg_name)

        # Validate value
        if not (isinstance(value, tuple(types))):
            raise InputException(
                f'Value provided for {arg_name} is not one of the expected types (value: {value}, types: {types})')

        return value

    @classmethod
    def validate_dir_name(cls, value, arg_name):
        cls.__validate_arg_name(arg_name)

        # Validate value
        blacklist = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

        value = str(value)

        if len(value) == 0:
            raise InputException(
                f'Directory name provided by {arg_name} is empty.')

        if len(value.strip()) is not len(value):
            print(Styler.stylize(
                f'Directory name provided by {arg_name} contains leading and trailing space. Proceeding to trim the following "{value}"', color='WARNING').encode())
            value = value.trim()

        for el in value:
            if el in BLACKLISTED_DIR_CHARS:
                raise InputException(
                    f'Directory name provided by {arg_name} is invalid. It may not contain the illegal character, "{el}".',  # nopep8
                    f'The provided directory name is "{value}".',
                    f'The list of blacklisted characters are {BLACKLISTED_DIR_CHARS}.',  # nopep8
                    f'If this directory path is generated from a sorter, please report or change to a different sorter.'
                )

        return value

    @classmethod
    def validate_dir_path(cls, value, arg_name):
        cls.__validate_arg_name(arg_name)

        # Validate value
        value = str(value)

        if len(value) == 0:
            raise InputException(
                f'Directory path provided by {arg_name} is empty.')

        if len(value.strip()) is not len(value):
            print(Styler.stylize(
                f'Directory path provided by {arg_name} contains leading and trailing space. Proceeding to trim the following "{value}"', color='WARNING')).encode()
            value = value.trim()

        modified_value = value.replace('/', '\\') if os.name == 'nt' else value
        if os.name == 'nt' and os.path.isabs(modified_value):
            modified_value = modified_value[2:]
        dir_names = [s for s in modified_value.split(os.path.sep) if s != ""]
        for dir_name in dir_names:
            try:
                cls.validate_dir_name(dir_name, arg_name)
            except InputException as e:
                raise InputException(
                    e, f'The invalid directory path is {value}')

        return modified_value
