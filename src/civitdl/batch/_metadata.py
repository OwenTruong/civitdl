from helpers.core.utils import Styler, InputException, ResourcesException, UnexpectedException, APIException, sprint, print_verbose

from helpers.sourcemanager import Id
from helpers.options import BatchOptions


class Metadata:
    __batchOptions = None
    __id = None

    model_name = None
    model_id = None
    version_id = None
    version_hashes = None

    model_dict = None
    version_dict = None

    nsfw = False
    nsfwLevel = None
    image_dicts = None
    image_download_urls = None
    model_download_url = None

    def __init__(self, id: Id, batchOptions: BatchOptions):
        self.__id = id
        self.__batchOptions = batchOptions

    def make_api_call(self):
        type = self.__id.type
        ids = self.__id.data

        if type == 'site' and len(ids) == 2:
            self.model_id = ids[0]
            self.version_id = ids[1]
            self.model_dict = self.__get_model_metadata()
            self.version_dict = self.__get_version_metadata()
        elif type == 'id' or (type == 'site' and len(ids) == 1):
            self.model_id = ids[0]
            self.model_dict = self.__get_model_metadata()
            if len(self.model_dict['modelVersions']) == 0:
                raise ResourcesException(
                    f'No model versions found from model id, {self.model_id}')
            self.version_dict = self.model_dict['modelVersions'][0]
            self.version_id = str(self.version_dict['id'])
        elif type == 'api':
            self.version_id = ids[0]
            self.version_dict = self.__get_version_metadata()
            self.model_id = str(self.version_dict['modelId'])
            self.model_dict = self.__get_model_metadata()
        else:
            raise InputException(
                f'Incorrect format sent ({ids}, {type}): "{self.__id.original}"')

        self.model_name = self.model_dict['name']

        self.nsfw = self.model_dict['nsfw']
        self.nsfwLevel = self.model_dict['nsfwLevel']

        print_verbose(f'nsfwLevel of model: {self.nsfwLevel}')
        print_verbose(f'Configurated nsfw mode: {self.__batchOptions.nsfw_mode}')  # nopep8

        self.image_dicts = []
        for image_dict in self.version_dict['images']:
            if image_dict['nsfwLevel'] <= 3:
                self.image_dicts.append(image_dict)
            elif (self.__batchOptions.nsfw_mode == '1' and (self.nsfw or image_dict['nsfwLevel'] <= self.nsfwLevel)) or self.__batchOptions.nsfw_mode == '2':
                self.image_dicts.append(image_dict)
        self.image_dicts = self.image_dicts[0:self.__batchOptions.max_images]

        print_verbose(f'nsfwLevel of images to download: {[image_dict["nsfwLevel"] for image_dict in self.image_dicts]}')  # nopep8

        self.image_download_urls = [image_dict['url']
                                    for image_dict in self.image_dicts]

        self.model_download_url = self.version_dict['downloadUrl']

        self.version_hashes = self.__get_version_hashes(
            self.version_dict, self.model_download_url)

        return self

    def __get_version_hashes(self, version_dict, download_url):
        files = version_dict['files']
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

    def __get_model_metadata(self):
        """Returns json object if request succeeds, else print error and returns None"""
        metadata_url = f'https://civitai.com/api/v1/models/{self.model_id}'
        metadata = self.__get_metadata(metadata_url)
        return metadata

    def __get_version_metadata(self):
        metadata_url = f'https://civitai.com/api/v1/model-versions/{self.version_id}'  # nopep8 # Linux issue
        metadata = self.__get_metadata(metadata_url)
        return metadata

    def __get_metadata(self, url: str):
        print_verbose('Requesting model metadata.')
        print_verbose(f'Metadata API Request URL: {url}')
        meta_res = self.__batchOptions.session.get(url, stream=True)

        print_verbose('Finished requesting model metadata.')
        if meta_res.status_code != 200:
            raise APIException(
                meta_res.status_code, f'Downloading metadata from CivitAI for "{self.__id.original}" failed when trying to request metadata from "{url}"')

        try:
            return meta_res.json()
        except Exception as e:
            raise UnexpectedException(
                'Unable to parse metadata from CivitAI (incorrect format provided by Civitai).', 'CivitAI might be under maintainence.',
                f'\nOriginal Error:\n       {e}')
