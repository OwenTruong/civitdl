
import os
import math
import csv
import re
from typing import Dict, Union

from helpers.core.utils import Styler, print_newlines, print_verbose, sprint
from helpers.core.constants import app_dirs
from helpers.core.iohelper import IOHelper

# TODO: Watch out for edge cases where one of the hash is empty.
# { '123456': { 'model_filepath': 'path', 'SHA256': 'hash1', 'BLAKE3': 'hash2' } }


class Cache:
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

    def __get_hash_dict(self) -> Union[None, Dict]:
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
            filepath = hash_dict.get('model_filepath')
            return None if not os.path.isfile(filepath) else filepath

    def get_hash_dict(self) -> Union[None, Dict]:
        return self.__get_hash_dict()

    def get_SHA256_hash(self) -> Union[None, str]:
        hash_dict = self.__get_hash_dict()
        if hash_dict:
            hash = hash_dict.get('SHA256', None)
            if hash != '':
                return hash


class CacheHelper:
    @classmethod
    def scan_models(cls, dir_path: str):
        data = {}
        regex = re.compile(
            r'mid_\d+-vid_(?P<vid>\d+)(?![\w.-]*(csv|txt|png|jpeg|jpg|json))')

        for root, _, filenames in os.walk(dir_path, followlinks=True):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                reg_res = regex.search(filepath)
                if reg_res:
                    vid = str(reg_res.group('vid'))
                    if vid in data:
                        continue  # already added vid to cache
                    cache = Cache(version_id=vid)
                    hash = cache.get_SHA256_hash()
                    hash_dict = None

                    if hash is None:
                        csv_filename = os.path.splitext[0] + '.csv'
                        csv_filepath = os.path.join(
                            os.path.dirname(filepath), csv_filename)

                        if os.path.exists(csv_filepath):
                            hash_dict = IOHelper.read_dict_from_csv(
                                csv_filepath)
                            hash = hash_dict.get('SHA256', None)

                    if hash is None:
                        print_newlines(Styler.stylize(
                            f"""SHA256 hash for the file path below was not found. Proceeding to skip file to protect against corruption.
                                - File Path: {filepath}
                            """, color='warning'))
                    elif IOHelper.compare_hash(filepath, hash):
                        if hash_dict is None:
                            hash_dict = cache.get_hash_dict()
                        cache.set_local_model_cache(
                            filepath, hash_dict if hash_dict else {})
                        print_verbose(Styler.stylize(
                            f'File path added to cache: {filepath}', color='info'))
                        data[vid] = filepath
                    else:
                        print_newlines(Styler.stylize(
                            f"""SHA256 hash for the file path below is incorrect. Proceeding to skip file to protect against corruption.
                                - File Path: {filepath}
                            """, color='warning'))
