from dataclasses import dataclass
import os
import re
from typing import List, Literal, Union, Optional

from helpers.core.utils import print_verbose, InputException, UnexpectedException

# modify id class to use getters and setters so that I can control how the data is being accessed
# modify id class to not use type.


class Id:
    """
    Id class may only be used externally for type hint and type checking
    """
    original: str
    model_id: Optional[str]
    version_id: Optional[str]

    def __init__(self):
        if type(self) == Id:
            raise UnexpectedException(f"only subclass of Id may be instantiated")  # nopep8


@dataclass
class _Id(Id):
    original: str
    model_id: Optional[str] = None
    version_id: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.original, str):
            raise UnexpectedException(f'Wrong data type for {self.original}')

        if self.model_id and not self.model_id.isdigit():
            raise UnexpectedException(f'Model id passed for {self.original} is not a valid model id. The model id passed: {self.model_id}')  # nopep8

        if self.version_id and not self.version_id.isdigit():
            raise UnexpectedException(f'Model id passed for {self.original} is not a valid model id. The version id passed: {self.version_id}')  # nopep8


class SourceManager:
    def __init__(self) -> None:
        pass

    def __get_comma_list(self, string: str) -> List[str]:
        return [input_str for input_str in string.replace(
            '\n', '').split(',') if input_str.strip() != '']

    def __use_parent_dir_if_exist(self, src: str, parent: Union[str, None]) -> str:
        return os.path.normpath(os.path.join(os.path.dirname(parent), src)) if parent else src

    def parse_src(self, str_li: List[str], parent: Union[str, None] = None) -> List[_Id]:
        res: List[_Id] = []
        for string in str_li:
            string = string.strip()

            if string.isdigit() and abs(int(string)) == int(string):
                model_id = string
                res.append(_Id(original=string, model_id=model_id))
            elif len(self.__get_comma_list(string)) > 1:
                arg_str_li = self.__get_comma_list(string)
                res.extend(self.parse_src(arg_str_li))
            elif 'civitai.com/api' in string:
                version_id_regex = r'(?<=models\/)\d+'
                version_id = re.search(version_id_regex, string)
                if version_id == None:
                    err = 'Incorrect format for the url provided' + \
                        (f' in {parent}: ' if parent else ': ') + string
                    raise InputException(err)
                version_id = version_id.group(0)
                res.append(_Id(original=string, version_id=version_id))
            elif 'civitai.com/models' in string:
                model_id = re.search(r'(?<=models\/)\d+', string)
                version_id = re.search(r'(?<=modelVersionId=)\d+', string)

                if model_id == None:
                    err = 'Incorrect format for the url/id provided' + \
                        (f' in {parent}: ' if parent else ': ') + string
                    raise InputException(err)
                model_id = model_id.group(0)

                if version_id:
                    version_id = version_id.group(0)
                    res.append(
                        _Id(original=string, model_id=model_id, version_id=version_id))
                else:
                    res.append(_Id(original=string, model_id=model_id))
            elif os.path.exists(self.__use_parent_dir_if_exist(string, parent)):
                string = self.__use_parent_dir_if_exist(string, parent)
                file_str = None

                with open(string, 'r', encoding='UTF-8') as file:
                    file_str = file.read().strip()
                if file_str == None:
                    raise UnexpectedException(
                        'Unknown exception while reading batchfile path.')
                str_li_res = self.__get_comma_list(file_str)
                print_verbose(str_li_res)
                res.extend(self.parse_src(str_li_res, parent=string))
            else:
                raise InputException(
                    f'Bad source provided: {string}', f'   Parent Batchfile Path: {parent}' if parent else None)

        return res
