import requests
import time
import sys
import copy
from useful_functions import *

# get the player index from command line arguments
player_index = int(sys.argv[1])

useful_functions = UsefulFunctions()
reached_goals = []
if player_index == 1:
    goals = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
    useful_functions.set_move_index([[1, -1], [0, 2], [1, 1], [0, -2]])
    enemy_player_index = 2
else:
    goals = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]
    useful_functions.set_move_index([[-1, -1], [-1, 1], [0, -2], [0, 2]])
    enemy_player_index = 1

def prune_moves_that_makes_us_be_further_away(pawn, moves):
    return moves

def evaluate(board, player_index):
    score = 0
    for goal in goals:
        if board[goal[0]][goal[1]] == player_index:
            score += 1

    if score == len(goals):
        return 10000

    for goal in goals:
        if goal in reached_goals:
            return -10000
        else:
            middle_goal = goal
            break
            
    for i in range(17):
        for j in range(25):
            if board[i][j] == player_index:
                score -= abs(i - middle_goal[0]) + abs(j - middle_goal[1])
    return score

def is_game_over(board):
    number_of_occupied_positions = 0
    number_of_self_occupied_positions = 0

    for goal in goals:
        if board[goal[0]][goal[1]] > 0:
            number_of_occupied_positions += 1
            if board[goal[0]][goal[1]] == 2:
                number_of_self_occupied_positions += 1

    if number_of_occupied_positions == len(goals) and number_of_self_occupied_positions != len(goals):
        return True

def minimax(board, depth, is_maximizing, alpha, beta, player_index):
    if is_game_over(board):
        return evaluate(copy.deepcopy(board), player_index)

    if depth == 0:
        return evaluate(copy.deepcopy(board), player_index)
    
    if is_maximizing:
        max_eval = -100000
        for pawn in useful_functions.get_pawns(copy.deepcopy(board), player_index):                
            valid_moves = useful_functions.get_valid_moves(copy.deepcopy(board), pawn)
            valid_moves = prune_moves_that_makes_us_be_further_away(pawn, valid_moves)
            for move in valid_moves:
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
        for pawn in useful_functions.get_pawns(copy.deepcopy(board), enemy_player_index):
            valid_moves = useful_functions.get_valid_moves(copy.deepcopy(board), pawn)
            valid_moves = prune_moves_that_makes_us_be_further_away(pawn, valid_moves)
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
    try:
        response = requests.get(f'http://localhost:5000/is_ai_turn/{player_index}')
        if response.json().get('is_ai_turn'):
            start_time = time.time()
            board = requests.get(f'http://localhost:5000/get_board').json()["board"]
            best_move = []
            best_eval = -100000
            best_pawn = []
            for pawn in useful_functions.get_pawns(copy.deepcopy(board), player_index):

                # check reached goals and add them to the list
                if pawn in goals:
                    if pawn not in reached_goals:
                        reached_goals.append(pawn)
                valid_moves = useful_functions.get_valid_moves(copy.deepcopy(board), pawn)
                valid_moves = prune_moves_that_makes_us_be_further_away(pawn, valid_moves)
                for move in valid_moves:
                    new_board = useful_functions.move(copy.deepcopy(board), pawn, move)
                    if new_board == False:
                        print("[MAIN] Invalid move")
                        sys.exit()
                    eval = minimax(copy.deepcopy(new_board), 2, False, -100000, 100000, player_index)
                    if eval > best_eval:
                        best_eval = eval
                        best_move = move
                        best_pawn = pawn

            finish_time = time.time()

            print(f"Moving: {best_pawn} -> {best_move}, Time taken: {finish_time - start_time}, Eval: {best_eval}")
            requests.post(f'http://localhost:5000/move/{best_pawn[0]}/{best_pawn[1]}/{best_move[0]}/{best_move[1]}')
    except Exception as e:
        print(e)
        

    time.sleep(0.25)