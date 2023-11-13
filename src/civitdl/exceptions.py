import json
from termcolor import colored


class CustomException(Exception):
    def __init__(self, error_type, *messages):
        res = ""
        res += colored(f'\n{self.__class__.__name__} ({error_type}):',
                       'red', attrs=['bold'])

        for message in messages:
            res += colored(f'\n         {message}',
                           'red')

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
