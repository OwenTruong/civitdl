#!/usr/bin/env python3

import sys
import traceback
from operator import itemgetter


from civitdl.helper.utils import run_in_dev
from civitconfig.data.setupJson import setupJson
from civitconfig.args.argparser import get_args


def main():
    try:
        setupJson()
        args = get_args()
        print(args)

    except Exception as e:
        print('---------')
        run_in_dev(traceback.print_exc)
        print(e)
        print('---------')
