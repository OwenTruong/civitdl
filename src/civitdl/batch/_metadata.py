from typing import Dict, List, Tuple, Optional
from helpers.core.utils import Styler, InputException, ResourcesException, UnexpectedException, APIException, sprint, print_verbose

from helpers.sourcemanager import Id
from helpers.options import BatchOptions

from requests import Session


# Convert id to appopriate format

# get metadata

class _MetadataFetcher:
    __original_id: str
    __session: Session

    def __init__(self, original_id: str, session: Session):
        self.__original_id = original_id
        self.__session = session

    def fetch(self, id: Id) -> Tuple[Tuple[dict, dict], Tuple[str, str]]:
        if id.version_id is not None:
            try:
                metadata = self.__get_version_model_metadata(id.version_id)
            except ResourcesException:
                if id.model_id is not None:
                    metadata = self.__get_model_version_metadata(
                        id.model_id, version_id=id.version_id)
        elif id.model_id is not None:
            metadata = self.__get_model_version_metadata(id.model_id)
        else:
            raise UnexpectedException(
                f'No model and version id found for "{id.original}"')

        return (metadata, (metadata[0]['id'], metadata[1]['id']))

    def __get_model_version_metadata(self, model_id: str, version_id: Optional[str] = None):
        model_dict = self.__get_model_metadata(model_id)
        key = 'modelVersions'

        if key not in model_dict:
            raise ResourcesException(
                f'{key} not in model metadata.'
            )
        elif not isinstance(model_dict[key], List):
            raise ResourcesException(
                f'{key} is not an iterable in model metadata.'
            )
        elif len(model_dict[key]) == 0:
            raise ResourcesException(
                f'No version metadata was found from model id, {model_id}')
        else:
            if version_id is None:
                return (model_dict, model_dict[key][0])

            for version_dict in model_dict[key]:
                if version_dict['id'] == version_id:
                    return (model_dict, version_dict)

            raise ResourcesException(
                f'Version id, {version_id}, does not exist for model id, {model_id}'  # nopep8
            )

    def __get_version_model_metadata(self, version_id: str):
        version_dict = self.__get_version_metadata(version_id)
        if version_dict['modelId'] is None:
            raise ResourcesException(
                f'Unable to recover model id from version id, {version_id}')
        else:
            return (self.__get_model_metadata(str(version_dict['modelId'])), version_dict)

    def __get_model_metadata(self, model_id: str):
        """Returns json object if request succeeds, else print error and returns None"""
        metadata_url = f'https://civitai.com/api/v1/models/{model_id}'
        metadata = self.__get_metadata(metadata_url)
        return metadata

    def __get_version_metadata(self, version_id: str):
        metadata_url = f'https://civitai.com/api/v1/model-versions/{version_id}'  # nopep8
        metadata = self.__get_metadata(metadata_url)
        return metadata

    def __get_metadata(self, url: str):
        print_verbose('Requesting model metadata.')
        print_verbose(f'Metadata API Request URL: {url}')
        meta_res = self.__session.get(url, stream=True)

        print_verbose('Finished requesting model metadata.')
        if meta_res.status_code != 200:
            raise APIException(
                meta_res.status_code, f'Downloading metadata from CivitAI for "{self.__original_id}" failed when trying to request metadata from "{url}"')

        try:
            return meta_res.json()
        except Exception as e:
            raise UnexpectedException(
                'Unable to parse metadata from CivitAI (incorrect format provided by Civitai).', 'CivitAI might be under maintainence.',
                f'\nOriginal Error:\n       {e}')


# extract data from metadata


class Metadata:
    __options_nsfw_mode: str
    __options_max_images: int
    __options_session: Session

    model_dict: Dict
    version_dict: Dict
    model_id: int
    version_id: int
    model_download_url: str

    model_name: str = 'unknown'
    version_hashes: Dict = {}

    nsfwLevel: int = -1
    image_dicts: List[Dict] = []
    image_download_urls: List[str] = []

    def __init__(self, nsfw_mode: str, max_images: int, session: Session):
        self.__options_nsfw_mode = nsfw_mode
        self.__options_max_images = max_images
        self.__options_session = session

    def make_api_call(self, id: Id):
        ((model_metadata, version_metadata), (model_id, version_id)) = _MetadataFetcher(
            original_id=id.original, session=self.__options_session).fetch(id)

        self.model_dict = model_metadata
        self.version_dict = version_metadata
        self.model_id = model_id
        self.version_id = version_id
        if 'downloadUrl' in self.version_dict and isinstance(self.version_dict['downloadUrl'], str) and self.version_dict['downloadUrl'] != '':
            self.model_download_url = self.version_dict['downloadUrl']
        else:
            raise ResourcesException(
                'Invalid download url received from CivitAI API!')

        # optional

        if 'name' in self.model_dict:
            self.model_name = self.model_dict['name']
        else:
            sprint(Styler.stylize(
                'Model name not found in metadata!', color='warning'))

        if 'nsfwLevel' in self.model_dict:
            self.nsfwLevel = self.model_dict['nsfwLevel']
        else:
            sprint(Styler.stylize(
                'Model name not found in metadata!', color='warning'))

        print_verbose(f'nsfwLevel of model: {self.nsfwLevel}')
        print_verbose(f'Configurated nsfw mode: {self.__options_nsfw_mode}')  # nopep8

        if 'images' in self.version_dict:
            sfw_level = 3
            try:
                # FIXME: There is a change that the sfw level will not be 3 or below in the future. I should make sfw level user configurable.
                for image_dict in self.version_dict['images']:
                    if 'nsfwLevel' not in image_dict:
                        sprint(Styler.stylize(
                            'nsfwLevel property not in image metadata!', color='warning'))
                        continue
                    elif (
                        image_dict['nsfwLevel'] <= sfw_level
                        or
                        (
                            self.__options_nsfw_mode == '1' and (
                                self.nsfwLevel == -1 or
                                image_dict['nsfwLevel'] <= self.nsfwLevel + 1
                            )
                        )
                        or
                        self.__options_nsfw_mode == '2'
                    ):
                        self.image_dicts.append(image_dict)
            except TypeError as err:
                sprint(Styler.stylize(err, color='warning'))

            print_verbose(f'Above NSFW threshold: {[dic for dic in self.image_dicts if dic["nsfwLevel"] > self.nsfwLevel + 1]}')  # nopep8
            print_verbose(f'Total images: {len(self.version_dict["images"])}')
            print_verbose(f'NSFW filtered total images: {len(self.image_dicts)}')  # nopep8

            len_of_image_dicts = len(self.image_dicts)
            self.image_dicts = [
                image_dict for image_dict in self.image_dicts if 'url' in image_dict]
            if len_of_image_dicts != len(self.image_dicts):
                sprint(Styler.stylize(
                    'Some or all images were removed due to being unable to parse metadata for the download url of the images!', color='warning'))
            self.image_dicts = self.image_dicts[0:self.__options_max_images]
        else:
            sprint(Styler.stylize(
                "Metadata of images do not exist in version metadata!", color='warning'))

        print_verbose(f'nsfwLevel of images to download: {[image_dict["nsfwLevel"] for image_dict in self.image_dicts]}')  # nopep8

        self.image_download_urls = [image_dict['url']
                                    for image_dict in self.image_dicts]

        if 'files' in self.version_dict:
            files = None
            try:
                files = list(self.version_dict['files'])
            except TypeError:
                sprint(Styler.stylize(
                    'files property in version metadata is not an iterable!', color='warning'))

            if files is not None:
                self.version_hashes = self.__get_version_hashes(
                    files, self.model_download_url)
        else:
            sprint(Styler.stylize(
                'files property not found in version metadata!', color='warning'))

        return self

    def __get_version_hashes(self, files, download_url):
        hashes = {}
        for file in files:
            if "downloadUrl" in file and file['downloadUrl'] == download_url:
                if isinstance(file['hashes'], dict):
                    hashes = file['hashes']
                else:
                    sprint(Styler.stylize(
                        'Hashes found in metadata is not a dictionary! There is an error with the API!', color='error'))
                break
        if hashes is {}:
            sprint(Styler.stylize('Hash not found in metadata.', color='warning'))
        elif "SHA256" not in hashes:
            sprint(Styler.stylize('SHA256 hash not found.', color='warning'))
        return hashes
