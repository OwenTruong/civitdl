from dataclasses import InitVar, dataclass, field
from datetime import datetime
import json
import os
import sys
import time
import math
import csv
import importlib.metadata
from typing import IO, Callable, Dict, Iterable, List, Union, Optional
import concurrent.futures
import requests
from tqdm import tqdm
from appdirs import AppDirs

from helpers.sorter.utils import import_sort_model
from helpers.sorter import basic, tags
from helpers.styler import Styler
from helpers.exceptions import CustomException, InputException, ResourcesException, UnexpectedException
from helpers.utils import print_verbose
from helpers.validation import Validation

# TODO: Watch out for edge cases where one of the hash is empty.
# { '123456': { 'model_filepath': 'path', 'SHA256': 'hash1', 'BLAKE3': 'hash2' } }


class Hash:
    __CACHE_COLUMNS = ['volume_id', 'model_filepath', 'SHA256', 'BLAKE3']
    __version_id: str
    __filepath: str
    __hashes_dict: Dict

    def __init__(self, version_id: str):
        self.__version_id = version_id
        version_id_num = int(version_id)

        app_dirs = AppDirs('civitdl', 'Owen Truong')
        dirpath = os.path.join(app_dirs.user_cache_dir,
                               'hashes', str(math.floor(version_id_num / 10000)))
        print(dirpath)
        filenum = math.floor(version_id_num / 100)
        filename = f'{filenum}.csv'
        self.__filepath = os.path.join(dirpath, filename)
        if not os.path.isfile(self.__filepath):
            os.makedirs(os.path.dirname(self.__filepath), exist_ok=True)
            with open(self.__filepath, 'w') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(self.__CACHE_COLUMNS)

        self.__hashes_dict = self.__read_from_csv()

    def __read_from_csv(self):
        hashes_dict = {}
        with open(self.__filepath, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                try:
                    row[3]
                    raise InputException(
                        f'Hash file is invalid. File contains rows with more than 3 columns.\nThe filepath for the invalid csv is "{self.__filepath}"')
                except:
                    hashes_dict[row[0]] = {
                        'model_filepath': row[1],
                        'SHA256': row[2],
                        'BLAKE3': row[3]
                    }
        return hashes_dict

    def __write_to_csv(self):
        with open(self.__filepath, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(
                self.__CACHE_COLUMNS)
            for key, value in self.__hashes_dict.items():
                csv_writer.writerow([
                    key,
                    value.get('model_filepath', ''),
                    value.get('SHA256', ''),
                    value.get('BLAKE3', '')
                ])

    def __get_hash_dict(self) -> Dict:
        return self.__hashes_dict.get(self.__version_id)

    def set_local_model_cache(self, model_filepath: str, hashes: Dict[str, str]) -> None:
        self.__hashes_dict[self.__version_id] = {
            'model_filepath': model_filepath,
            'SHA256': hashes.get('SHA256', ''),
            'BLAKE3': hashes.get('BLAKE3', '')
        }
        self.__write_to_csv()

    def get_local_model_path(self) -> Union[None, str]:
        hash_dict = self.__get_hash_dict()

        if hash_dict is None:
            print(Styler.stylize(
                f'Cache of model with version id {self.__version_id} not found.', color='info'))
            return None
        else:
            filepath = hash_dict['model_filepath']
            return None if not os.path.isfile(filepath) else filepath
