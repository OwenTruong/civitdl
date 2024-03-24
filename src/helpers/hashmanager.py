
import os
import math
import csv
from typing import Dict, Union

from helpers.core.utils import Styler, print_verbose, sprint
from helpers.core.constants import app_dirs

# TODO: Watch out for edge cases where one of the hash is empty.
# { '123456': { 'model_filepath': 'path', 'SHA256': 'hash1', 'BLAKE3': 'hash2' } }


class HashManager:
    __CACHE_COLUMNS = ['volume_id', 'model_filepath', 'SHA256', 'BLAKE3']
    __version_id: str
    __filepath: str
    __hashes_dict: Dict

    def __init__(self, version_id: str):
        self.__version_id = version_id
        version_id_num = int(version_id)

        dirpath = os.path.join(app_dirs.user_cache_dir,
                               'hashes', str(math.floor(version_id_num / 10000)))
        print_verbose(dirpath)
        filenum = math.floor(version_id_num / 100)
        filename = f'{filenum}.csv'
        self.__filepath = os.path.join(dirpath, filename)
        if not os.path.isfile(self.__filepath):
            os.makedirs(os.path.dirname(self.__filepath), exist_ok=True)
            with open(self.__filepath, 'w', encoding='UTF-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(self.__CACHE_COLUMNS)

        self.__hashes_dict = self.__read_from_csv()

    def __read_from_csv(self):
        hashes_dict = {}
        with open(self.__filepath, 'r', encoding='UTF-8') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                if row == []:
                    continue
                hashes_dict[row[0]] = {
                    'model_filepath': row[1],
                    'SHA256': row[2],
                    'BLAKE3': row[3]
                }
        return hashes_dict

    def __write_to_csv(self):
        with open(self.__filepath, 'w', encoding='UTF-8') as f:
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
            'model_filepath': os.path.abspath(model_filepath),
            'SHA256': hashes.get('SHA256', ''),
            'BLAKE3': hashes.get('BLAKE3', '')
        }
        self.__write_to_csv()

    def get_local_model_path(self) -> Union[None, str]:
        hash_dict = self.__get_hash_dict()

        if hash_dict is None:
            sprint(Styler.stylize(
                f'Cache of model with version id {self.__version_id} not found.', color='info'))
            return None
        else:
            filepath = hash_dict['model_filepath']
            return None if not os.path.isfile(filepath) else filepath
