__author__ = 'sam'

import sys
import os
import logging
import json
import argparse

logging.basicConfig(format='%(asctime)s %(levelname)s: (%(name)s) %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def list_folder(dir_path, full_path=False):
    dir_list = []
    for item in os.listdir(dir_path):
        item_path = '%s\\%s' % (dir_path, item)
        if os.path.isdir(item_path):
            dir_list += list_folder(item_path)
        else:
            if not full_path:
                dir_list.append(item_path)
            else:
                dir_list.append(os.path.abspath(item_path))
    return dir_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-f', '--fullpath', action='store_true')
    parser.set_defaults(fullpath=False)
    args = parser.parse_args()

    files_list = list_folder(args.path, args.fullpath)

    with open('%s\\%s.json' % (os.getcwd(), os.path.basename(args.path)), 'w') as f:
        json.dump(files_list, f)

if __name__ == '__main__':
    sys.exit(main())
