import random
import sys
from typing import TextIO

SYMBOLS_PROBABILITY = {'x': 1, '0': 1, '.': 398}

_SYMBOLS = [x for x in SYMBOLS_PROBABILITY for _ in range(SYMBOLS_PROBABILITY[x])]
random.shuffle(_SYMBOLS)


def write_board(size: int, f: TextIO):
    for i in range(size):
        line = []
        for j in range(size):
            line.append(random.choice(_SYMBOLS))
        line.append('\n')
        f.write(''.join(line))


if __name__ == '__main__':
    # Run as `python board_generator.py 300 > board.txt`
    size = int(sys.argv[1])
    write_board(size, sys.stdout)
