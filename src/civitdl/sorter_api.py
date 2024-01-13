from helpers.validation import Validation
from dataclasses import dataclass


@dataclass
class SorterConfig:
    parent_dir_name: str
    parent_dir_path: str
    metadata_dir_path: str
    image_dir_path: str
    prompt_dir_path: str

    def __post_init__(self):
        self.parent_dir_name = Validation.validate_dir_name(
            self.parent_dir_name, 'sorter')

        self.parent_dir_path = Validation.validate_dir_path(
            self.parent_dir_path, 'sorter')

        self.metadata_dir_path = Validation.validate_dir_path(
            self.metadata_dir_path, 'sorter')

        self.image_dir_path = Validation.validate_dir_path(
            self.image_dir_path, 'sorter')

        self.prompt_dir_path = Validation.validate_dir_path(
            self.prompt_dir_path, 'sorter')
