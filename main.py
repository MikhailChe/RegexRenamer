import argparse
import logging
from sys import stdout

import json


def read_config(filename: str):
    with open(filename) as f:
        return json.load(f)


def validate_config(config: dict):
    if not isinstance(config, dict):
        raise ValueError('Incorrect config schema. Top level should be dict')
    if any(map(lambda k: not isinstance(k, str), config.keys())):
        raise ValueError('Incorrect config schema. Keys should be of type string')
    if any(map(lambda k: not isinstance(config[k], str), config.keys())):
        raise ValueError('Incorrect config schema. Values should be of type string')
    return config


def main(options):
    config = validate_config(read_config(options.config))
    import regexrenamer.renamer
    regexrenamer.renamer.rename_bunch(
        path=options.path,
        config=config,
        output=options.output,
        dry=options.dry,
        makedirs=options.makedirs,
        force_overwrite=options.force,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename files')
    parser.add_argument(
        'path',
        default='.',
        type=str,
        help='Path to directory containing files to be renamed',
    )
    parser.add_argument(
        '--output',
        default='./renamed',
        type=str,
        help='Path to output directory',
    )
    parser.add_argument(
        '--force',
        '-f',
        action='store_true',
        help='Overwrite file if it already exists',
    )
    parser.add_argument(
        '--config',
        default=None,
        required=True,
        help='Path to config file'
    )
    parser.add_argument(
        '--dry',
        action='store_true',
        help='Dry run. Dont rename anything. Use with -v'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='count',
        help='Verbose output',
    )
    parser.add_argument(
        '--makedirs',
        action='store_true',
        help='Automatically create output directory if it doesnt exist'
    )
    args = parser.parse_args()

    root_logger = logging.getLogger()
    root_logger.addHandler(logging.StreamHandler(stdout))
    root_logger.setLevel(logging.ERROR)
    if args.verbose:
        if args.verbose == 1:
            root_logger.setLevel(logging.WARNING)
        if args.verbose == 2:
            root_logger.setLevel(logging.INFO)
        elif args.verbose == 3:
            root_logger.setLevel(logging.DEBUG)
    main(args)
