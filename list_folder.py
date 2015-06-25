__author__ = 'sam'

import sys
import os
import json
import argparse

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

def write_list(path, output, fullpath, directories):
    files_list = list_folder(path, fullpath, directories)

    output_path = output if output else '%s/%s.json' % (os.getcwd(), os.path.basename(path))
    with open(output_path, 'w') as f:
        json.dump(files_list, f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('output', nargs='?', default=None)
    parser.add_argument('-f', '--fullpath', action='store_true')
    parser.set_defaults(fullpath=False)
    parser.add_argument('-d', '--directories', action='store_true')
    parser.set_defaults(directories=False)
    args = parser.parse_args()

    write_list(args.path, args.output, args.fullpath, args.directories)

if __name__ == '__main__':
    sys.exit(main())
