import os
import shutil
import sys
import time
import csv
from typing import IO, Callable, Iterable, Union

from ._ui.styler import Styler, InputException, UnexpectedException
from .utils import get_progress_bar, sprint


class IOHelper:

    # Level 0 #

    @staticmethod
    def createDirsIfNotExist(dirpaths):
        for dirpath in dirpaths:
            os.makedirs(dirpath, exist_ok=True)

    @staticmethod
    def delete_file_if_exists(file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                raise UnexpectedException(
                    f"Error deleting file {file_path}: {e}")

    @staticmethod
    def write_contents(file: IO, content_chunks: Iterable, limit_rate: Union[int, None] = None, update_pb: Union[Callable[[int], None], None] = None):
        last_chunk_time = time.perf_counter()
        for content in content_chunks:
            file.write(content)
            bytes_downloaded = len(content)

            download_time = time.perf_counter() - last_chunk_time
            speed = bytes_downloaded / \
                download_time if download_time != 0 else float('inf')
            if limit_rate is not None and limit_rate != 0 and speed > limit_rate:
                time_to_sleep = (bytes_downloaded / limit_rate) - download_time
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)

            if update_pb:
                update_pb(bytes_downloaded)
            last_chunk_time = time.perf_counter()

    @staticmethod
    def read_dict_from_csv(filepath: str):
        csv_dict = {}

        with open(filepath, 'r', encoding='UTF-8') as f:
            csv_iterator = csv.reader(f)
            next(csv_iterator)
            for row in csv_iterator:
                try:
                    row[2]
                    raise InputException(
                        f'CSV file is invalid. File contains rows with more than two columns.\nThe filepath for the invalid csv is "{filepath}"')
                except:
                    csv_dict[row[0]] = row[1]

        return csv_dict

    # Level 1 #
    @classmethod
    def write_to_file(cls, filepath: str, content_chunks: Iterable, mode: str = None, limit_rate: Union[int, None] = 0, encoding: Union[str, None] = None, overwrite: bool = True, use_pb: bool = False, total: float = 0, desc: str = None):
        """Uses content_chunks to write to filepath bit by bit. If use_pb is enabled, it is recommended to set total kwarg to the length of the file to be written."""
        progress_bar = get_progress_bar(total, desc) if use_pb else None

        def update_progress_bar(bytes_downloaded):
            if progress_bar:
                progress_bar.update(bytes_downloaded)

        if not overwrite and os.path.exists(filepath):
            if (progress_bar):
                progress_bar.close()
            sprint(Styler.stylize(
                f'File already exists at "{filepath}"', color='info'))
        else:
            temp_dirpath = os.path.join(os.path.dirname(
                filepath), '.tmp')
            temp_filepath = os.path.join(
                temp_dirpath, os.path.basename(filepath))
            os.makedirs(temp_dirpath, exist_ok=True)
            try:
                with open(temp_filepath, mode if mode != None else 'w', encoding=encoding) as file:
                    cls.write_contents(file, content_chunks,
                                       limit_rate, update_progress_bar)
                shutil.move(temp_filepath, filepath)
                shutil.rmtree(temp_dirpath)
            except Exception as e:
                sprint('Existance: ', temp_dirpath, temp_filepath,
                       os.path.exists(temp_filepath), file=sys.stderr)
                if os.path.exists(temp_dirpath):
                    shutil.rmtree(temp_dirpath)
                raise e
            if (progress_bar):
                progress_bar.close()

    @classmethod
    def write_to_files(cls, dirpath: str, basenames: Iterable, content_chunks_list: Iterable[Iterable], mode: str = None, encoding: Union[str, None] = None, use_pb: bool = False, total: float = 0, desc: str = None):
        """Write content to multiple files in dirpath. If use_pb is enabled, it is recommended to set total kwarg to the number of files being written."""
        progress_bar = get_progress_bar(total, desc) if use_pb else None
        for basename, content_chunks in zip(basenames, content_chunks_list):
            filepath = os.path.join(dirpath, basename)
            with open(filepath, mode if mode != None else 'w', encoding=encoding) as file:
                cls.write_contents(file, content_chunks)
                if (progress_bar):
                    progress_bar.update(1)
        if (progress_bar):
            progress_bar.close()
