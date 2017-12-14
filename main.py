import math
import multiprocessing
import sys
from typing import List, TextIO

import finder


def read_board(f: TextIO) -> List[List[str]]:
    """Creates a game board from a text file."""
    board = []
    for i, line in enumerate(f.readlines()):
        row = list(line.rstrip('\n'))
        if i > 0 and len(row) != len(board[i - 1]):
            raise ValueError(f'size of the row {i} differs from the row {i - 1}')
        board.append(row)

    if len(board) != len(board[0]):
        raise ValueError('the board is not square')

    return board


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        processes_num = int(sys.argv[2])
    except IndexError:
        processes_num = multiprocessing.cpu_count() * 2

    with open(filename, 'r') as f:
        board = read_board(f)
        n = len(board)
        if processes_num == 1:
            print('Processing in 1 process')
            print(finder.find_in_board(board))
        else:
            found_event = multiprocessing.Event()
            found_result = multiprocessing.Queue(maxsize=1)
            # Divide the board among the processes.
            processes: List[multiprocessing.Process] = []
            chunk_size = math.ceil(n / processes_num)
            for i in range(processes_num):
                first_row = 0 if i == 0 else i * chunk_size - (finder.FRAME_SIZE - 1)
                last_row = i * chunk_size + chunk_size + (finder.FRAME_SIZE - 1)
                p = multiprocessing.Process(
                    target=finder.find_in_board,
                    args=(board[first_row:last_row], found_event, found_result, first_row))
                processes.append(p)

            print(f'Starting {len(processes)} processes')
            for p in processes:
                p.start()

            for p in processes:
                p.join()

            if found_event.is_set():
                # TODO: returned position is relative to the board that was given to the worker. Fix it.
                print(found_result.get())
            else:
                print('No winning combination found.')
