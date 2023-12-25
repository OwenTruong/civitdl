from enum import Enum
from typing import List, Literal


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
    PRIMARY = '\033[32m'
    SECONDARY = '\033[34m'
    SUCCESS = '\033[35m'
    INFO = '\033[36m'


class _BGColors(_FormatEnum):
    # Background colors
    EXCEPTION = '\033[41m'
    WARNING = '\033[43m'

    PRIMARY = '\033[42m'
    SECONDARY = '\033[44m'
    SUCCESS = '\033[45m'
    INFO = '\033[46m'


class Styler(Enum):
    RESET = '\033[0m'  # Reset to default text and background color

    @classmethod
    def stylize(cls, string: str, styles: List[str] = None, color: str = None, bg_color: str = None):
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
            color_attr = _Colors.get_attribute(color)
            if color_attr:
                res += color_attr.value
            else:
                raise Exception(
                    f'The following color "{color}" does not exist.')

        if bg_color:
            bg_attr = _BGColors.get_attribute(bg_color)
            if bg_attr:
                res += bg_attr.value
            else:
                raise Exception(
                    f'The following background color "{bg_color}" does not exist.')

        res += string
        res += cls.RESET.value
        return res
