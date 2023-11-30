import numpy as np

import evaluation
import game_functions as gf


class Expectimax:
    def __init__(self, board):
        self.DEPTH_BASE_PARAM = 1 # You may change this parameter to scale the depth to which the agent searches.
        self.SCALER_PARAM = 400 # You may change this parameter to scale depth to which the agent searches.
        self.board = board

    def get_depth(self, move_number):
        """
        Returns the depth to which the agent should search for the given move number.
        ...
        :type move_number: int
        :param move_number: The current move number.
        :return: The depth to which the agent should search for the given move number.
        """
        # TODO: Complete get_depth function to return the depth to which the agent should search for the given move number.
        # Hint: You may need to use the DEPTH_BASE_PARAM constant.
        return 2
        # if len(gf.get_empty_cells(self.board)[0]) == 3:
        #     return 3
        # else:
        #     return 2

    def ai_move(self, board, move_number):
        depth = self.get_depth(move_number)
        score, action = self.expectimax(board, depth, 1)
        return action

    def expectimax(self, board: np.ndarray, depth: int, turn: int):
        """
        Returns the best move for the given board state and turn.
        ...
        :type turn: int
        :type depth: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param depth: Depth to which agent takes actions for each move
        :param turn: The turn of the agent. 1 for AI, 0 for computer.
        :return: Returns the best move and score we can obtain by taking it, for the given board state and turn.
        """
        
        # TODO: Complete expectimax function to return the best move and score for the given board state and turn.
        # Hint: You may need to implement minimizer_node and maximizer_node functions.
        # Hint: You may need to use the evaluation.evaluate_state function to score leaf nodes.
        # Hint: You may need to use the gf.terminal_state function to check if the game is over.
        
        if gf.terminal_state(board) or depth == 0:
            return (evaluation.evaluate_state(board), gf.get_moves()[0])

        if turn == 1:
            return self.maximizer_node(board, depth)
        else:
            return self.chance_node(board, depth)
            


    def maximizer_node(self, board: np.ndarray, depth: int):
        """
        Returns the best move for the given board state and turn.
        ...
        :type depth: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param depth: Depth to which agent takes actions for each move
        :return: Returns the move with highest score, for the given board state.
        """
        
        # TODO: Complete maximizer_node function to return the move with highest score, for the given board state.
        # Hint: You may need to use the gf.get_moves function to get all possible moves.
        # Hint: You may need to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may need to use the np.copy function to create a copy of the board.
        # Hint: You may need to use the np.inf constant to represent infinity.
        # Hint: You may need to use the max function to get the maximum value in a list.
        
        max_score = -np.inf
        action = None

        for new_board, direction in gf.get_all_possible_moves(board):
            score, _ = self.expectimax(new_board, depth - 1, 0) # one move has been made so reduce depth and give the turn to machine
            if score > max_score:
                max_score = score
                action = gf.get_moves()[direction]

        return (max_score, action)
    

    def chance_node(self, board: np.ndarray, depth: int):
        """
        Returns the expected score for the given board state and turn.
        ...
        :type depth: int
        :type board: np.ndarray
        :param board: The board state for which the expected score is to be found.
        :param depth: Depth to which agent takes actions for each move
        :return: Returns the expected score for the given board state.
        """
        
        # TODO: Complete chance_node function to return the expected score for the given board state.
        # Hint: You may need to use the gf.get_empty_cells function to get all empty cells in the board.
        # Hint: You may need to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may need to use the np.copy function to create a copy of the board.
        
        weighted_score = 0
        # new_board = np.ndarray.copy(board)
        row_arr, col_arr = gf.get_empty_cells(board)
        num_empty_cells = len(row_arr)
        for i in range(num_empty_cells):
            r = row_arr[i]
            c = col_arr[i]
            board[r][c] = 2
            score, _ = self.expectimax(board, depth, 1)
            weighted_score += (0.9 / num_empty_cells) * score
            board[r][c] = 4
            score, _ = self.expectimax(board, depth, 1)
            weighted_score += (0.1 / num_empty_cells) * score
            board[r][c] = 0
            
        return (weighted_score, None)
