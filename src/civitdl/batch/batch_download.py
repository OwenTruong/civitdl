import time
import traceback
from typing import List

from ._model import Model

from helpers.core.utils import Styler, APIException, get_version, print_exc, print_verbose, run_verbose, sprint
from helpers.sourcemanager import SourceManager
from helpers.options import BatchOptions

__version__ = get_version()


def _pause(sec):
    print_verbose('Pausing for 3 seconds...')
    time.sleep(sec)
    print_verbose('Waking up!')


def batch_download(source_strings: List[str], rootdir: str, batchOptions: BatchOptions):
    """Batch downloads model from CivitAI one by one."""

    source_manager = SourceManager()

    for id in source_manager.parse_src(source_strings):

        iter = 0
        while True:
            try:
                model = Model(dst_root_path=rootdir,
                              batchOptions=batchOptions).download(id=id)
                _pause(batchOptions.pause_time)
                break
            except Exception as e:
                sprint('---------')
                run_verbose(traceback.print_exc)
                print_exc(e, '\n')
                sprint('---------')
                _pause(batchOptions.pause_time)
                # if not isinstance(e, APIException):
                #     break
                if iter < batchOptions.retry_count:
                    sprint(Styler.stylize(
                        'Retrying to download the current model...', color='info'))
                    iter += 1
                else:
                    sprint(Styler.stylize(
                        f'Max retry of {batchOptions.retry_count} reached. Skipping the current model...', color='info'))
                    break
