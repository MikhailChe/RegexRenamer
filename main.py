import argparse

import ujson


def read_config(filename: str):
    with open(filename) as f:
        return ujson.load(f)


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
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename files')
    parser.add_argument(
        'path',
        default='.',
        description='Path to directory containing files to be renamed'
    )
    parser.add_argument(
        '--output',
        default='./renamed',
        required=True,
        description='Output directory'
    )
    parser.add_argument(
        '--config',
        default=None,
        required=True,
        description='Path to config file'
    )
    args = parser.parse_args()
    main(args)
