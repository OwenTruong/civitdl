
import argparse
import getpass


class PwdAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        mypass = getpass.getpass(prompt='Key: ')
        setattr(namespace, self.dest, mypass)


class ConfirmAction(argparse.BooleanOptionalAction):
    def __call__(self, parser, namespace, value, option_string=None):
        response = input(
            'Are you sure you want to move the current configuration to trash, and reset with default? (y/n): ').strip().lower()
        if response not in ('y', 'yes'):
            parser.error(f"Reset declined. Exiting.")

        super().__call__(parser, namespace, value, option_string)
