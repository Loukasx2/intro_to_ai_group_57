import requests
import time
import sys
import copy
import yaml
from useful_functions import *

# load config file
with open("config.yaml", "r") as yamlfile:
    cfg = yaml.safe_load(yamlfile)

DEPTH = cfg["depth"]
ALPHA_BETA_PRUNING = cfg["alpha_beta_pruning"]

number_of_explored_board_states = 0

# get the player index from command line arguments
player_index = int(sys.argv[1])

useful_functions = UsefulFunctions()
reached_goals = []
if player_index == 1:
    # useful_functions.set_move_index([[1, -1], [0, 2], [1, 1], [0, -2]])
    enemy_goals, goals = useful_functions.get_starting_positions()
    enemy_player_index = 2
else:
    # useful_functions.set_move_index([[-1, -1], [-1, 1], [0, -2], [0, 2]])
    goals, enemy_goals = useful_functions.get_starting_positions()
    enemy_player_index = 1

reached_goals = []
furthest_goal_index = 0
furthest_goal = goals[furthest_goal_index]

def evaluate(board, player_index, depth):
    score = 0

    score_for_pawns_in_goals = 0
    for goal in goals:
        if board[goal[0]][goal[1]] == player_index:
            score_for_pawns_in_goals += 1

    if score == len(goals):
        return 10000 * (depth + 1)

    score_for_distance_to_goal = 0
    for i in range(BOARD_SIZE_X):
        for j in range(BOARD_SIZE_Y):
            if board[i][j] == player_index:
                score_for_distance_to_goal -= abs(i - furthest_goal[0]) + abs(j - furthest_goal[1])

    score_for_pawns_on_own_goal = 0
    for enemy_goal in enemy_goals:
        if board[enemy_goal[0]][enemy_goal[1]] == player_index:
            score_for_pawns_on_own_goal -= 10

    # print(f"Score: {score_for_pawns_in_goals} + {score_for_distance_to_goal} + {score_for_pawns_on_own_goal}")

    score = score_for_pawns_in_goals + score_for_distance_to_goal + score_for_pawns_on_own_goal

    global number_of_explored_board_states
    number_of_explored_board_states += 1

    return score

def did_i_win(board):
    number_of_occupied_positions = 0
    number_of_self_occupied_positions = 0

    for goal in goals:
        if board[goal[0]][goal[1]] > 0:
            number_of_occupied_positions += 1
            if board[goal[0]][goal[1]] == enemy_player_index:
                number_of_self_occupied_positions += 1

    if number_of_occupied_positions == len(goals) and number_of_self_occupied_positions != len(goals):
        return True
    
def did_enemy_win(board):
    number_of_occupied_positions = 0
    number_of_self_occupied_positions = 0

    for goal in enemy_goals:
        if board[goal[0]][goal[1]] > 0:
            number_of_occupied_positions += 1
            if board[goal[0]][goal[1]] == player_index:
                number_of_self_occupied_positions += 1

    if number_of_occupied_positions == len(enemy_goals) and number_of_self_occupied_positions != len(enemy_goals):
        return True

def minimax(board, depth, is_maximizing, alpha, beta, player_index):
    if did_i_win(board):
        return 10000 * (depth + 1)
    
    if did_enemy_win(board):
        return -10000 * (depth + 1)

    if depth == 0:
        return evaluate(copy.deepcopy(board), player_index, depth)
    
    if is_maximizing:
        max_eval = -100000
        for pawn in useful_functions.get_pawns(copy.deepcopy(board), player_index):   
            if pawn not in reached_goals:             
                valid_moves = useful_functions.get_valid_moves(copy.deepcopy(board), pawn)
                for move in valid_moves:
                    new_board = useful_functions.move(copy.deepcopy(board), pawn, move)
                    if new_board == False:
                        print("[[MAX]] Invalid move")
                        sys.exit()
                    eval = minimax(copy.deepcopy(new_board), depth - 1, False, alpha, beta, player_index)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha and ALPHA_BETA_PRUNING:
                        break
        return max_eval
    else:
        min_eval = 100000
        for pawn in useful_functions.get_pawns(copy.deepcopy(board), enemy_player_index):
            valid_moves = useful_functions.get_valid_moves(copy.deepcopy(board), pawn)
            for move in valid_moves:
                new_board = useful_functions.move(copy.deepcopy(board), pawn, move)
                if new_board == False:
                    print("[[MIN]] Invalid move")
                    sys.exit()
                eval = minimax(copy.deepcopy(new_board), depth - 1, True, alpha, beta, player_index)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha and ALPHA_BETA_PRUNING:
                    break
        return min_eval

calc_time_history = []

while not requests.get(f'http://localhost:5000/is_over').json()["over"]:
    try:
        response = requests.get(f'http://localhost:5000/is_ai_turn/{player_index}')
        is_ai_turn = response.json().get('is_ai_turn')
        if is_ai_turn:
            number_of_explored_board_states = 0
            start_time = time.time()
            board = requests.get(f'http://localhost:5000/get_board').json()["board"]
            best_move = []
            best_eval = -100000
            best_pawn = []
            for pawn in useful_functions.get_pawns(copy.deepcopy(board), player_index):
                if pawn not in reached_goals:
                    valid_moves = useful_functions.get_valid_moves(copy.deepcopy(board), pawn)
                    for move in valid_moves:
                        new_board = useful_functions.move(copy.deepcopy(board), pawn, move)
                        if new_board == False:
                            print("[MAIN] Invalid move")
                            sys.exit()
                        eval = minimax(copy.deepcopy(new_board), DEPTH, False, -100000, 100000, player_index)
                        if eval > best_eval:
                            best_eval = eval
                            best_move = move
                            best_pawn = pawn

            finish_time = time.time()
            calc_time_history.append(finish_time - start_time)

            print(f"Moving: {best_pawn} -> {best_move}, Time taken: {finish_time - start_time}, Eval: {best_eval}")
            requests.post(f'http://localhost:5000/move/{best_pawn[0]}/{best_pawn[1]}/{best_move[0]}/{best_move[1]}')
            if best_move in goals:
                    if best_move not in reached_goals and best_move == furthest_goal:
                        reached_goals.append(best_move)
                        furthest_goal_index += 1
                        furthest_goal = goals[furthest_goal_index]
            mean_time = sum(calc_time_history) / len(calc_time_history)

            # print(f"Mean time: {mean_time}")
            # print(f"Number of explored board states: {number_of_explored_board_states}")
        time.sleep(0.25)
    except Exception as e:
        pass

print("Game over!")

# Add to csv type file the mean time and the board configuration (number of checkers and board size), as well as cfg board size and number of rows with pawns. Add also the AI player index and the game winner.
# If player index is 1, the AI is the first player.
board = requests.get(f'http://localhost:5000/get_board').json()["board"]
with open("results.csv", "a") as file:
    file.write(f"{mean_time},{cfg['board_size']},{cfg['number_of_rows_with_pawns']},{player_index},{did_i_win(board)},{did_enemy_win(board)}\n")
    file.close()
