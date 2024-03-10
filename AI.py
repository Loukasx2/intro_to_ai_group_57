import requests
import time
import sys
import copy
from useful_functions import *

# get the player index from command line arguments
player_index = int(sys.argv[1])

if player_index == 1:
    goals = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
else:
    goals = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]
useful_functions = UsefulFunctions()

def evaluate(board, player_index):
    score = 0
    for goal in goals:
        if board[goal[0]][goal[1]] == player_index:
            score += 1

    #distnce to goal[4]
    middle_goal = goals[4]
    for i in range(17):
        for j in range(25):
            if board[i][j] == player_index:
                score -= abs(i - middle_goal[0]) + abs(j - middle_goal[1])
    return score

def minimax(board, depth, is_maximizing, alpha, beta, player_index):
    board = board.copy()

    if depth == 0:
        return evaluate(copy.deepcopy(board), player_index)
    
    if is_maximizing:
        max_eval = -100000
        for pawn in useful_functions.get_pawns(copy.deepcopy(board), player_index):
            for move in useful_functions.get_valid_moves(copy.deepcopy(board), pawn):
                new_board = useful_functions.move(copy.deepcopy(board), pawn, move)
                if new_board == False:
                    print("[[MAX]] Invalid move")
                    sys.exit()
                eval = minimax(copy.deepcopy(new_board), depth - 1, False, alpha, beta, player_index)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = 100000
        for pawn in useful_functions.get_pawns(copy.deepcopy(board), 1):
            valid_moves = useful_functions.get_valid_moves(copy.deepcopy(board), pawn)
            for move in valid_moves:
                new_board = useful_functions.move(copy.deepcopy(board), pawn, move)
                if new_board == False:
                    print("[[MIN]] Invalid move")
                    sys.exit()
                eval = minimax(copy.deepcopy(new_board), depth - 1, True, alpha, beta, player_index)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

while True:
    response = requests.get(f'http://localhost:5000/is_ai_turn/{player_index}')
    if response.json().get('is_ai_turn'):
        board = requests.get(f'http://localhost:5000/get_board').json()["board"]
        best_move = []
        best_eval = -100000
        best_pawn = []
        for pawn in useful_functions.get_pawns(copy.deepcopy(board), player_index):
            for move in useful_functions.get_valid_moves(copy.deepcopy(board), pawn):
                new_board = useful_functions.move(copy.deepcopy(board), pawn, move)
                if new_board == False:
                    print("[MAIN] Invalid move")
                    sys.exit()
                eval = minimax(copy.deepcopy(new_board), 2, False, -100000, 100000, player_index)
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
                    best_pawn = pawn

        requests.post(f'http://localhost:5000/move/{best_pawn[0]}/{best_pawn[1]}/{best_move[0]}/{best_move[1]}')
        

    time.sleep(0.25)