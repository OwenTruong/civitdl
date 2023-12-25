
import argparse
import getpass
from gettext import gettext
import sys

from helpers.styler import Styler


class PwdAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        mypass = getpass.getpass(prompt='Key: ')
        setattr(namespace, self.dest, mypass)


class ConfirmAction(argparse.BooleanOptionalAction):
    def __call__(self, parser, namespace, value, option_string=None):
        response = input(
            'Are you sure you want to move the current configuration to trash, and reset with default? (y/N): ').strip().lower()
        if response not in ('y', 'yes'):
            parser.error(f"Reset declined. Exiting.")

        super().__call__(parser, namespace, value, option_string)


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
