import sys
sys.path.append(sys.argv[-1])
import os.path as pth
from glob import glob
from backup_utility import *


def main():
    path = [project('wins test'), component('sinWave'), date()]
    set_default(__file__)
    if len(sys.argv) > 2:
        folder = sys.argv[-2]
    else:
        print('No watched folder supplied')
        return

    file_filter = '*.txt'
    files = glob(pth.join(folder, file_filter))
    files = list(filter(old_file, files))
    if files:
        print('Look at these beautiful files!')
    else:
        print('No old text files')

    for f in files:
        with open(f, 'r') as fil:
            contents = fil.read()
            nums = [int(s) for s in contents.strip().split(',')]
            print(sum(nums))

    if files:
        move(files, path)


if __name__ == '__main__':
    main()
