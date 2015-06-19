__author__ = 'sam'

import sys
import os
import json
import argparse

from .logger import initialize_logging

log = initialize_logging()

def list_folder(dir_path, full_path=False, directories=False):
    dir_list = []
    for item in os.listdir(dir_path):
        item_path = '%s/%s' % (dir_path, item)
        if full_path:
            item_path = os.path.abspath(item_path)
        item_path = item_path.replace('\\', '/')
        if os.path.isdir(item_path):
            if directories:
                dir_list.append(item_path)
            dir_list += list_folder(item_path, full_path, directories)
        else:
            if not directories:
                dir_list.append(item_path)
    return dir_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('output', nargs='?', default=None)
    parser.add_argument('-f', '--fullpath', action='store_true')
    parser.set_defaults(fullpath=False)
    parser.add_argument('-d', '--directories', action='store_true')
    parser.set_defaults(directories=False)
    args = parser.parse_args()

    files_list = list_folder(args.path, args.fullpath, args.directories)

    output_path = args.output if args.output else '%s/%s.json' % (os.getcwd(), os.path.basename(args.path))
    with open(output_path, 'w') as f:
        json.dump(files_list, f)

if __name__ == '__main__':
    sys.exit(main())
