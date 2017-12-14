import math
import multiprocessing
import sys
from typing import List, TextIO

import finder


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        processes_num = int(sys.argv[2])
    except IndexError:
        processes_num = multiprocessing.cpu_count() * 2

    with open(filename, 'r') as f:
        # Get the lines count.
        n = sum(1 for _ in f)
        if processes_num == 1:
            print('Processing in 1 process')
            print(finder.find_in_board(filename))
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
                    args=(filename, first_row, last_row, found_event, found_result))
                processes.append(p)

            print(f'Starting {len(processes)} processes')
            for p in processes:
                p.start()

            for p in processes:
                p.join()

            if found_event.is_set():
                print(found_result.get())
            else:
                print('No winning combination found.')
