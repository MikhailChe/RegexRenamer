import os
import re
import shutil
from typing import List, Dict

import logging

log = logging.getLogger(__name__)


def rename_bunch(
    path: str, config: Dict[str, str], output: str,
    dry: bool, makedirs: bool, force_overwrite: bool,
):
    filenames = os.listdir(path)
    for origin, destination in find_replacements(filenames, config):
        log.info('%s -> %s', os.path.join(path, origin), os.path.join(output, destination))
        if makedirs:
            if not dry:
                os.makedirs(os.path.dirname(os.path.join(output, destination)), exist_ok=True)
        do_copy = False
        if os.path.exists(os.path.join(output, destination)):
            if not force_overwrite:
                log.warning('File %s already exists in directory %s', destination, output)
            else:
                do_copy = True
        else:
            do_copy = True
        if do_copy:
            if not dry:
                shutil.copyfile(
                    os.path.join(path, origin),
                    os.path.join(output, destination)
                )


def find_replacements(filenames: List[str], config: Dict[str, str]):
    for filename in filenames:
        for r in config.keys():
            if re.fullmatch(r, filename):
                yield filename, re.sub(r, config[r], filename)
