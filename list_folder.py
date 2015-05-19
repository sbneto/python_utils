__author__ = 'sam'

import sys
import os
import logging
import json

logging.basicConfig(format='%(asctime)s %(levelname)s: (%(name)s) %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def list_folder(dir_path):
    dir_list = []
    for item in os.listdir(dir_path):
        item_path = '%s\\%s' % (dir_path, item)
        if os.path.isdir(item_path):
            dir_list += list_folder(item_path)
        else:
            dir_list.append(item_path)
    return dir_list

def main(argv):

    if len(argv) < 2 or not os.path.exists(argv[1]):
        print("Usage: list_folder.py [list_path]")
        return 1

    list_path = os.path.abspath(argv[1])
    files_list = list_folder(list_path)

    with open('%s\\%s.json' % (os.getcwd(), os.path.basename(list_path)), 'w') as f:
        json.dump(files_list, f)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
