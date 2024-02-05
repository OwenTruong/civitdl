
import argparse
from gettext import gettext
import os
import sys
import getpass
import warnings
try:
    import msvcrt
except:
    None

from helpers.core.utils import Styler


def windows_getpass(prompt=""):
    api_key = ""
    while True:
        char = msvcrt.getch().decode('utf-8')
        if char == '\r' or char == '\n':
            break
        elif char == '\x03':  # Ctrl+C
            raise KeyboardInterrupt
        elif char == '\b':
            api_key = api_key[:-1]
        else:
            api_key += char
    return api_key


class PwdAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        mypass = values
        if mypass is None:
            mypass = windows_getpass(prompt='Key: ') if os.name == 'nt' else getpass.getpass(
                prompt='Key: ')
        setattr(namespace, self.dest, mypass)


class ColoredArgParser(argparse.ArgumentParser):

    def print_usage(self, file=None):
        if file is None:
            file = sys.stdout
        self._print_message(self.format_usage()[0].upper() +
                            self.format_usage()[1:],
                            file, 'warning')

    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        self._print_message(self.format_help()[0].upper() +
                            self.format_help()[1:],
                            file, 'info')

    def _print_message(self, message: str, file=None, color=None, styles=None):
        if message:
            if file is None:
                file = sys.stderr
            if color is None:
                file.write(message)
            else:
                file.write(
                    Styler.stylize(f'{message.strip()}\n', color=color, styles=styles))

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr,
                                'exception')
        sys.exit(status)

    def error(self, message):
        self.print_usage(sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self.exit(2, gettext('%(prog)s: Error: %(message)s\n') % args)


# Copied from argparse for compatibility reasons below python v3.9
_deprecated_default = object()


class BooleanOptionalAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest,
                 default=None,
                 type=_deprecated_default,
                 choices=_deprecated_default,
                 required=False,
                 help=None,
                 metavar=_deprecated_default):

        _option_strings = []
        for option_string in option_strings:
            _option_strings.append(option_string)

            if option_string.startswith('--'):
                option_string = '--no-' + option_string[2:]
                _option_strings.append(option_string)

        # We need `_deprecated` special value to ban explicit arguments that
        # match default value. Like:
        #   parser.add_argument('-f', action=BooleanOptionalAction, type=int)
        for field_name in ('type', 'choices', 'metavar'):
            if locals()[field_name] is not _deprecated_default:
                warnings._deprecated(
                    field_name,
                    "{name!r} is deprecated as of Python 3.12 and will be "
                    "removed in Python {remove}.",
                    remove=(3, 14))

        if type is _deprecated_default:
            type = None
        if choices is _deprecated_default:
            choices = None
        if metavar is _deprecated_default:
            metavar = None

        super().__init__(
            option_strings=_option_strings,
            dest=dest,
            nargs=0,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, not option_string.startswith('--no-'))

    def format_usage(self):
        return ' | '.join(self.option_strings)


class ConfirmAction(BooleanOptionalAction):
    def __call__(self, parser, namespace, value, option_string=None):
        response = input(
            'Are you sure you want to move the current configuration to trash, and reset with default? (y/N): ').strip().lower()
        if response not in ('y', 'yes'):
            parser.error(f"Reset declined. Exiting.")

        super().__call__(parser, namespace, value, option_string)
