# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
# remove empty directories
# ----------

import os
import sys
from contextlib import suppress

assert sys.getdefaultencoding() == 'utf-8', 'encoding utf-8 is required.'

NT_CACHE_FILES = {
    'Thumbs.db'
}

def _listdir(path: str):
    return [(name, os.path.join(path, name)) for name in os.listdir(path)]

def _try_remove_file(path: str):
    with suppress(PermissionError):
        with suppress(FileNotFoundError):
            os.remove(path)
            print('removed %s' % path)
        return True
    return False

def try_remove_empty_directory(root: str, include_self: bool):
    '''
    try remove empty directory.
    '''

    with suppress(PermissionError): # raise when call os.listdir(...)
        try:
            items = _listdir(root)
        except FileNotFoundError:
            return True

        if sum(int(not try_remove_empty_directory(x[1], True)) for x in items if os.path.isdir(x[1])):
            return False

        files_items = [x for x in items if os.path.isfile(x[1])]
        files_names = {x[0] for x in files_items}
        if (NT_CACHE_FILES & files_names) != files_names: # all files are cache files
            return False

        if sum(int(not _try_remove_file(x[1])) for x in files_items):
            return False

        if include_self and not os.listdir(root):
            try:
                with suppress(FileNotFoundError):
                    os.rmdir(root)
                    print('removed %s' % root)
                return True
            except OSError as e:
                print('removing %s catch %s' % (root, e))

    return False

def main(argv=None):
    if argv is None:
        argv = sys.argv

    args = argv[1:]
    if args:
        try_remove_empty_directory(args[0], False)

if __name__ == '__main__':
    main()
