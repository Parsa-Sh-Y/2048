import numpy as np
import math

import game_functions as gf


def evaluate_state(board: np.ndarray) -> float:
    """
    Returns the score of the given board state.
    :param board: The board state for which the score is to be calculated.
    :return: The score of the given board state.
    """
    # TODO: Complete evaluate_state function to return a score for the current state of the board
    # Hint: You may need to use the np.nonzero function to find the indices of non-zero elements.
    # Hint: You may need to use the gf.within_bounds function to check if a position is within the bounds of the board.
    
    if gf.check_for_win(board):
        return np.inf
    elif gf.check_for_loss(board):
        return -10000
    
    result = 0  

    difference = 0
    for r in range(1, 4):
        if board[r][3] == 0 or board[r - 1][3]:
            continue
        difference += abs(board[r - 1][3] - board[r][3])

    for c in range(2, -1, -1):
        if board[0][c] == 0 or board[0][c + 1] == 0:
            difference += abs(board[0][c + 1] - board[0][c])

    for r in range(1, 4):
        for c in range(2, -1, -1):
            if board[r][c] == 0:
                continue
            if board[r - 1][c] != 0:
                difference += abs(board[r - 1][c] - board[r][c])
            if board[r][c + 1] != 0:
                difference += abs(board[r][c + 1] - board[r][c])

    # Give high values to top row squares
    for c in range(4):
        result += board[0][c] * 2**(c + 1)

    # Find the maximum value and take logarithm from all the squares and add them together
    # The logarithm will encourage the AI to merge squares and lose less points
    sum_log = 0
    max = 0
    for r in range(4):
        for c in range(4):
            num = board[r][c]
            if num > max:
                if num == 0:
                    pass
                elif num == 2:
                    sum_log += 2
                else:
                    sum_log += math.log2(num)
                max = num

    
    result += 20 * (board[0][3] - max) # Keep the square with maximum value at the top right corner
    result -= difference
    result -= 3 * sum_log
    return result

    
