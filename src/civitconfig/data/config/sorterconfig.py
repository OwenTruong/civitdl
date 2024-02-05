import os
import shutil
import sys
from helpers.core.utils import InputException, ResourcesException, getDate, print_exc, sprint
from helpers.sorter.utils import import_sort_model
from .config import Config


class SorterConfig(Config):

    def __init__(self, *args):
        super(SorterConfig, self).__init__(*args)

    def _copyPyFile(self, filepath) -> str:
        dst_filename = f'{getDate()}.py'
        dstpath = os.path.join(
            self._sorters_dir_path, dst_filename)
        try:
            shutil.copy2(filepath, dstpath)
            return dstpath
        except Exception as e:
            sprint('Source: ', filepath, file=sys.stderr)
            sprint('Destination: ', dstpath, file=sys.stderr)
            raise e

    def _uncopyPyFile(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            raise ResourcesException(
                'Unable to uncopy python file (or delete it from program) because it does not exist')

    def _trashPyFile(self, filepath):
        filename = os.path.basename(filepath)
        trashpath = os.path.join(
            self._sorters_trash_dir_path, filename)
        if os.path.exists(filepath):
            shutil.move(filepath, trashpath)
            return trashpath
        else:
            raise ResourcesException(
                'Unable to trash python file because it does not exist.')

    def _untrashPyFile(self, trashpath):
        filename = os.path.basename(trashpath)
        filepath = os.path.join(
            self._sorters_dir_path, filename)
        if os.path.exists(trashpath):
            shutil.move(trashpath, filepath)
            return filepath
        else:
            raise ResourcesException(
                'Unable to untrash python file because it does not exist.')

    def trashPyFiles(self, pyfile_paths):
        trashfile_paths = []
        try:
            for pyfile_path in pyfile_paths:
                trashfile_paths.append(self._trashPyFile(pyfile_path))
            return trashfile_paths
        except Exception as e:
            for trashfile_paths in trashfile_paths:
                self._untrashPyFile(trashfile_paths)
            raise e

    def untrashPyFiles(self, trashfile_paths):
        pyfile_paths = []
        try:
            for trashfile_path in trashfile_paths:
                pyfile_paths.append(self._untrashPyFile(trashfile_path))
            return pyfile_paths
        except Exception as e:
            for pyfile_path in pyfile_paths:
                self._trashPyFile(pyfile_path)
            raise e

    def addSorter(self, name, filepath):
        sorters = self.getSortersList()

        if name == 'tags' or name == 'basic':
            raise InputException(f'Sorter with name "{name}" is reserved.')

        if '/' in name:
            raise InputException(f'Sorter name may not contain "/": {name}')

        if name in [sorter[0] for sorter in sorters]:
            raise InputException(f'Sorter with name "{name}" already exist.')

        desc = import_sort_model(
            filepath).__doc__ or "Description not provided"

        # First, we save python file (if exception, need to undo)
        filepath = self._copyPyFile(filepath)

        # Then, we edit config
        config = None
        try:
            config = self._getConfig()
            config['sorters'].append([name, desc, filepath])
        except:
            self._uncopyPyFile(filepath)
            raise e

        # Lastly, we save config
        try:
            self._saveConfig(config)
        except Exception as e:
            self._uncopyPyFile(filepath)
            raise e

    def deleteSorter(self, name):
        sorters = self.getSortersList()

        if name == 'tags' or name == 'basic':
            raise InputException(
                f'Sorter with name "{name}" can not be deleted.')

        if name not in [sorter[0] for sorter in sorters]:
            raise InputException(f'Sorter with name "{name}" does not exist.')

        sorter_py_path = [sorter[2]
                          for sorter in sorters if sorter[0] == name][0]

        # First, we edit config
        config = self._getConfig()
        config['sorters'] = [
            sorter for sorter in config['sorters'] if sorter[0] != name]

        # Then, we delete file (if exception, need to undo)
        resources_error_was_raised = False
        trashpath = None
        try:
            trashpath = self._trashPyFile(sorter_py_path)
        except Exception as e:
            if type(e).__name__ == 'ResourcesException':
                print_exc(e)
                resources_error_was_raised = True
            else:
                raise e

        # Lastly, we make changes to config
        try:
            self._saveConfig(config)
        except Exception as e:
            if not resources_error_was_raised:
                self._untrashPyFile(trashpath)
            raise e
