import math
import os.path as path
import time


def main():
    folder = path.join(path.expanduser('~'), 'Desktop', 'test')
    signal = [math.sin(i/math.pi) for i in range(2e4)]
    for i in range(3e4):
        with open('{}.txt'.format(i), 'w') as f:
            f.write(','.join(signal))
        time.sleep(1)
    

if __name__ == '__main__':
    main()
