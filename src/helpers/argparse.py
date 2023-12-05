
import argparse
import getpass


class PwdAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        mypass = getpass.getpass(prompt='Key: ')
        setattr(namespace, self.dest, mypass)