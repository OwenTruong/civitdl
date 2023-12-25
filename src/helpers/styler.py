from enum import Enum
from typing import List, Literal

# Private


class _FormatEnum(Enum):
    @classmethod
    def get_attribute(cls, format: str):
        format = format.upper()
        for attr in cls:
            if format == attr.name:
                return attr


class _Style(_FormatEnum):
    # Text styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class _Colors(_FormatEnum):
    # Text colors
    EXCEPTION = '\033[31m'
    WARNING = '\033[33m'
    SUCCESS = '\033[32m'

    PRIMARY = '\033[34m'
    SECONDARY = '\033[35m'
    INFO = '\033[36m'


class _BGColors(_FormatEnum):
    # Background colors
    EXCEPTION = '\033[41m'
    WARNING = '\033[43m'
    SUCCESS = '\033[42m'

    PRIMARY = '\033[44m'
    SECONDARY = '\033[45m'
    INFO = '\033[46m'


def _color_generator():
    color = 'primary'
    while True:
        if color == 'primary':
            color = 'secondary'
            yield 'primary'
        else:
            color = 'primary'
            yield 'secondary'


_color_iter = _color_generator()
_bgcolor_iter = _color_generator()


# Public / Exports


class Styler(Enum):
    RESET = '\033[0m'  # Reset to default text and background color

    @classmethod
    def _get_main_color_attr(cls, color: str):
        color = color.upper()
        if color == 'MAIN':
            color = cls._get_next_color()
        elif color in cls._get_main_color_list():
            raise Exception(
                f'Can not directly access PRIMARY or SECONDARY color.')

        return _Colors.get_attribute(color)

    @classmethod
    def _get_main_bgcolor_attr(cls, bgcolor: str):
        bgcolor = bgcolor.upper()
        if bgcolor == 'MAIN':
            bgcolor = cls._get_next_bgcolor()
        elif bgcolor in cls._get_main_color_list():
            raise Exception(
                f'Can not directly access PRIMARY or SECONDARY background color.')

        return _BGColors.get_attribute(bgcolor)

    @staticmethod
    def _get_next_color():
        return next(_color_iter)

    @staticmethod
    def _get_next_bgcolor():
        return next(_bgcolor_iter)

    @staticmethod
    def _get_main_color_list():
        return ['PRIMARY', 'SECONDARY']

    @classmethod
    def stylize(cls, string: str, color: str = None, bg_color: str = None, styles: List[str] = None):
        res = ''

        if styles:
            for style in styles:
                style_attr = _Style.get_attribute(style)
                if style_attr:
                    res += style_attr.value
                else:
                    raise Exception(
                        f'The following style "{style}" does not exist.')

        if color:
            color_attr = cls._get_main_color_attr(color)
            if color_attr:
                res += color_attr.value
            else:
                raise Exception(
                    f'The following color "{color}" does not exist.')

        if bg_color:
            bg_attr = cls._get_main_bgcolor_attr(bg_color)
            if bg_attr:
                res += bg_attr.value
            else:
                raise Exception(
                    f'The following background color "{bg_color}" does not exist.')

        res += string
        res += cls.RESET.value
        return res
