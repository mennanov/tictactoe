"""Find 3x3 winning combination fot a Tic Tac Toe game."""
import multiprocessing
from typing import List, Union, NewType, Tuple

BoardType = List[List[str]]
Event = NewType('Event', multiprocessing.Event)

FRAME_SIZE = 3


def find_in_frame(board: BoardType) -> bool:
    """Detect if there is a winning combination in a frame of size FRAME_SIZExFRAME_SIZE (square)."""
    n = len(board)
    if n != FRAME_SIZE or any(len(r) != FRAME_SIZE for r in board):
        raise ValueError(f'field of size {FRAME_SIZE}x{FRAME_SIZE} is expected')

    x_row, o_row = ['x'] * FRAME_SIZE, ['0'] * FRAME_SIZE

    field_transposed = list(zip(*board))
    # Find rows combinations.
    for i in range(n):
        # Horizontal case.
        if board[i] == x_row or board[i] == o_row:
            return True
        # Vertical case.
        if field_transposed[i] == x_row or field_transposed[i] == o_row:
            return True

    # Diagonal cases.
    diag_lt_rb = [board[i][i] for i in range(n)]
    if diag_lt_rb == x_row or diag_lt_rb == o_row:
        return True

    diag_lb_rt = [board[i][n - i - 1] for i in range(n)]
    if diag_lb_rt == x_row or diag_lb_rt == o_row:
        return True

    return False


def read_board(filename: str, line_start=0, line_end=None) -> List[List[str]]:
    """Creates a game board from a text file."""
    with open(filename) as f:
        board = []
        for i, line in enumerate(f.readlines()):
            if i < line_start:
                continue
            if line_end is not None and i >= line_end:
                break
            row = list(line.rstrip('\n'))
            board.append(row)

    return board


def find_in_board(filename: str, line_start=0, line_end=None,
                  found_event: Union[Event, None] = None,
                  result: multiprocessing.Queue = None) -> Union[Tuple[Tuple[int, int], BoardType], None]:
    """Find winning combinations in a board of any size by moving a frame and looking for them there.

    Returns:
        Position of the winning combination and a frame if any.
    """
    board = read_board(filename, line_start, line_end)
    n = len(board)

    for i in range(n - FRAME_SIZE):
        for j in range(n - FRAME_SIZE):
            if found_event is not None and found_event.is_set():
                # Gracefully stop the processing.
                return None
            frame = [board[k][j:j + FRAME_SIZE] for k in range(i, i + FRAME_SIZE)]
            if find_in_frame(frame):
                if found_event is not None:
                    found_event.set()
                if result is not None:
                    result.put(((i + line_start, j), frame))
                return (i + line_start, j), frame
    return None
