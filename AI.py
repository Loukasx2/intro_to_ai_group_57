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
    goals = [[8, 4], [7, 3], [7, 5], [6, 2], [6, 4], [6, 6]]
    enemy_goals = [[0, 4], [1, 3], [1, 5], [2, 2], [2, 4], [2, 6]]
    # useful_functions.set_move_index([[1, -1], [0, 2], [1, 1], [0, -2]])
    enemy_player_index = 2
else:
    goals = [[0, 4], [1, 3], [1, 5], [2, 2], [2, 4], [2, 6]]
    enemy_goals = [[8, 4], [7, 3], [7, 5], [6, 2], [6, 4], [6, 6]]
    # useful_functions.set_move_index([[-1, -1], [-1, 1], [0, -2], [0, 2]])
    enemy_player_index = 1

reached_goals = []
furthest_goal_index = 0
furthest_goal = goals[0]

def prune_moves_that_makes_us_be_further_away(pawn, moves):
    return moves

def evaluate(board, player_index):
    score = 0
    goals_available = copy.deepcopy(goals)
    for goal in goals:
        if board[goal[0]][goal[1]] == player_index:
            score += 1
            goals_available.remove(goal)

    if score == len(goals):
        return 10000

    for i in range(BOARD_SIZE_X):
        for j in range(BOARD_SIZE_Y):
            if board[i][j] == player_index:
                # # find closes avaialble goal
                # closest_distance = None
                # for goal in goals_available:
                #     distance_to_goal = abs(i - goal[0]) + abs(j - goal[1])
                #     if closest_distance == None or distance_to_goal < closest_distance:
                #         closest_distance = distance_to_goal
                # score -= closest_distance
                score -= abs(i - furthest_goal[0]) + abs(j - furthest_goal[1])

    # penalize pawns in the enemy goals
    for enemy_goal in enemy_goals:
        if board[enemy_goal[0]][enemy_goal[1]] == player_index:
            score -= 10

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
            if pawn not in reached_goals:             
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
    response = requests.get(f'http://localhost:5000/is_ai_turn/{player_index}')
    if response.json().get('is_ai_turn'):
        start_time = time.time()
        board = requests.get(f'http://localhost:5000/get_board').json()["board"]
        best_move = []
        best_eval = -100000
        best_pawn = []
        for pawn in useful_functions.get_pawns(copy.deepcopy(board), player_index):

            # check reached goals and add them to the list
            if pawn not in reached_goals:
                print(f"Reached goal: {pawn}")
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
        if best_move in goals:
                if best_move not in reached_goals and best_move == furthest_goal:
                    reached_goals.append(best_move)
                    furthest_goal_index += 1
                    furthest_goal = goals[furthest_goal_index]
    

    time.sleep(0.25)