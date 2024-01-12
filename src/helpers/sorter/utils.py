from typing import Callable, Dict, List
import importlib.util


def import_sort_model(path: str) -> Callable[[Dict, Dict, str, str], List[str]]:
    spec = importlib.util.spec_from_file_location('sorter', path)
    sorter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sorter)
    return sorter.sort_model
