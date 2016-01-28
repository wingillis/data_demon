import math
import os.path as path
import time


def main():
    folder = path.join(path.expanduser('~'), 'Desktop', 'test')
    signal = [str(int(math.sin(i/math.pi))) for i in range(2000)]
    for i in range(30000):
        with open(path.join(folder,'{}.txt'.format(i)), 'w') as f:
            f.write(','.join(signal))
        signal = [str(int(s)+1) for s in signal]
        time.sleep(1)


if __name__ == '__main__':
    main()
