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
    log.info('Found files: %s', filenames)

    for origin, destination in find_replacements(filenames, config):
        if makedirs:
            if not dry:
                os.makedirs(os.path.abspath(os.path.join(output)), exist_ok=True)
        else:
            if not os.path.exists(os.path.abspath(os.path.join(output))):
                log.error(
                    'Directory %s doesnt exist. Use --makedirs flag to force directory creation',
                    os.path.abspath(output),
                )
                return
        log.info('%s -> %s', os.path.join(path, origin), os.path.join(output, destination))
        do_copy = False
        if os.path.exists(os.path.join(output, destination)):
            if not force_overwrite:
                log.error('File %s already exists in directory %s', destination, output)
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
                log.debug('Filename %s match regex %s', filename, r)
                yield filename, re.sub(r, config[r], filename)
