import os
import re
import shutil


def rename_bunch(path: str, config: dict, output: str):
    filenames = os.dirpath(path)
    for origin, destination in find_replacements(filenames, config):
        shutil.copy(
            os.path.join(path, origin),
            os.path.join(output, destination)
        )


def find_replacements(filenames: list[str], config: dict):
    for filename in filenames:
        for r in config.keys():
            if re.fullmatch(r, filename):
                yield filename, re.sub(r, config[r], filename)
