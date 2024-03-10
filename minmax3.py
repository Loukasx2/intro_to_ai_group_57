import requests
import random
import time
import sys

MAX_VALUE = 10000000
MIN_VALUE = -10000000

def evaluate(move, initial_pawn_position):
    score = 0

    if move == goals[0]:
        print("Goal reached")
        return MAX_VALUE
    elif move in goals[1:3] and initial_pawn_position not in goals[0:3]:
        return MAX_VALUE
    elif move in goals[3:6] and initial_pawn_position not in goals[0:6]:
        return MAX_VALUE
    elif move in goals[6:10] and initial_pawn_position not in goals[0:10]:
        return MAX_VALUE

    if move in goals or initial_pawn_position in goals:
        return MIN_VALUE

    for goal in goals:
        distance_to_goal = abs(move[0] - goal[0]) + abs(move[1] - goal[1])
        initial_pawn_distance_to_goal = abs(initial_pawn_position[0] - goal[0]) + abs(initial_pawn_position[1] - goal[1])
        score += -distance_to_goal + initial_pawn_distance_to_goal * 1.2
    return score

def minmax(moves, depth, is_maximizing):
    if depth == 0:
        return evaluate(moves, goals)

    if is_maximizing:
        max_eval = MIN_VALUE

        return max_eval
    else:
        min_eval = MAX_VALUE

        return min_eval

# get the player index from command line arguments
player_index = int(sys.argv[1])

if player_index == 1:
    goals = [[16, 12], [15, 11], [15, 13],[14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
else:
    goals = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]

while True:
    try:
        response = requests.get(f'http://localhost:5000/is_ai_turn/{player_index}')
        if response.json().get('is_ai_turn'):
            pawns_response = requests.get(f'http://localhost:5000/get_player_pawns/{player_index}')
            pawns = pawns_response.json().get('pawns')

            best_move = None
            best_pawn = None
            best_score = -10000
            for pawn in pawns:
                # if pawn in goals:
                #     continue
                possible_moves = requests.get(f'http://localhost:5000/get_moves/{pawn[0]}/{pawn[1]}').json().get('moves')
                for move in possible_moves:
                    score = evaluate(move, pawn)
                    if score >= best_score:
                        best_score = score
                        best_move = move
                        best_pawn = pawn

            print(f'[{player_index}] Best move: {best_move} for pawn {best_pawn} with score {best_score}')

            move_response = requests.post(f'http://localhost:5000/move/{best_pawn[0]}/{best_pawn[1]}/{best_move[0]}/{best_move[1]}')
            # if move_response.status_code == 200:
            #     print("Move successful.")
            # else:
            #     print("Invalid move.")

        # wait for 1 second
        # time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(e)
