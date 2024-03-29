import argparse
import json
import logging
import os
from sys import stdout

import regexrenamer.renamer

log = logging.getLogger(__name__)


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
    log.debug('Reading and validating config file %s', options.config)
    config = validate_config(read_config(options.config))
    log.debug('Read valid config %s', config)
    regexrenamer.renamer.rename_bunch(
        path=options.path,
        config=config,
        output=options.output,
        dry=options.dry,
        makedirs=options.makedirs,
        force_overwrite=options.force,
    )


def config_and_start():
    APP_DIR = os.path.dirname(os.path.realpath(__file__))

    DEFAULT_CONFIG_PATH = os.path.join(APP_DIR, 'configs', 'gerbers.json')

    parser = argparse.ArgumentParser(description='Rename files')
    parser.add_argument(
        'path',
        default='.',
        nargs='?',
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
        default=DEFAULT_CONFIG_PATH,
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
    options = parser.parse_args()

    root_logger = logging.getLogger()
    root_logger.addHandler(logging.StreamHandler(stdout))
    root_logger.setLevel(logging.ERROR)
    if options.verbose:
        if options.verbose == 1:
            root_logger.setLevel(logging.WARNING)
        if options.verbose == 2:
            root_logger.setLevel(logging.INFO)
        elif options.verbose == 3:
            root_logger.setLevel(logging.DEBUG)
    log.debug('APP_DIR: %s', APP_DIR)
    log.debug('DEFAULT_CONFIG_PATH: %s', DEFAULT_CONFIG_PATH)
    log.debug('Using config path %s', options.config)
    main(options)


if __name__ == '__main__':
    config_and_start()
