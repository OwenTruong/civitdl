import json
from .styler import Styler


class CustomException(Exception):
    def __init__(self, error_type, *messages):
        res = ""

        res += Styler.stylize(f'\n{self.__class__.__name__} ({error_type}):',
                              color='exception', styles=['bold'])

        for message in messages:
            res += Styler.stylize(f'\n         {message}', color='exception')

        super().__init__(res)


class InputException(CustomException):
    def __init__(self, *messages):
        super().__init__('Bad Inputs', *messages)


class ResourcesException(CustomException):
    def __init__(self, *messages):
        super().__init__('Resources Not Found', *messages)


class APIException(CustomException):
    def __init__(self, status_code, *messages):
        super().__init__(f'API Status Code {status_code}', *messages)


class NotImplementedException(CustomException):
    def __init__(self, *messages):
        super().__init__('Feature Not Implemented', *messages)


class UnexpectedException(CustomException):
    def __init__(self, *messages):
        super().__init__('Unexpected Error', *messages)
