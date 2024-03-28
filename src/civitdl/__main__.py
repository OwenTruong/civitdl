import traceback

from .batch.batch_download import batch_download, BatchOptions
from .args.argparser import get_args

from helpers.core.utils import print_verbose, run_verbose, print_exc, set_verbose, sprint


def main():
    try:
        args = get_args()

        if args['verbose']:
            set_verbose(True)
        else:
            set_verbose(False)

        tempargs = args.copy()
        tempargs.pop('api_key')
        print_verbose('Arguments: ', str(tempargs))

        batchOptions = BatchOptions(
            sorter=args['sorter'],
            max_images=args['max_images'],
            nsfw_mode=args['nsfw_mode'],
            api_key=args['api_key'],

            with_prompt=args['with_prompt'],
            without_model=args['without_model'],
            limit_rate=args['limit_rate'],
            retry_count=args['retry_count'],
            pause_time=args['pause_time'],

            cache_mode=args['cache_mode'],
            model_overwrite=args['model_overwrite'],

            with_color=args['with_color'],
            verbose=args['verbose']
        )

        batch_download(
            source_strings=args['source_strings'],
            rootdir=args['rootdir'],
            batchOptions=batchOptions
        )

    except Exception as e:
        sprint('---------')
        run_verbose(traceback.print_exc)
        print_exc(e)
        sprint('---------')
