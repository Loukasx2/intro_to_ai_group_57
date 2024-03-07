import requests
import random
import time
import sys

def evaluate_move(move, goals):
    """
    Evaluate a move based on the distance to the goals.
    """
    score = 0
    for goal in goals:
        distance = abs(move[0] - goal[0]) + abs(move[1] - goal[1])
        score += distance
    return score

def choose_best_move(available_moves, goals, current_position):
    """
    Choose the move with the highest score based on the evaluation function.
    """
    best_move = None
    best_score = float('inf')  # Initialize best_score to positive infinity
    for move in available_moves:
        # Check if move puts the pawn on a goal
        if move in goals:
            # If pawn is already on a goal, skip move unless necessary
            if current_position not in goals:
                score = evaluate_move(move, goals)
            else:
                # If pawn is already on a goal and it's necessary to move, prioritize this move
                score = 0
        else:
            score = evaluate_move(move, goals)
        if score < best_score:
            best_move = move
            best_score = score
    return best_move

# get the player index from command line arguments
player_index = int(sys.argv[1])

if player_index == 1:
    goals = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
else:
    goals = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]

while True:
    try:
        response = requests.get(f'http://localhost:5000/is_ai_turn/{player_index}')
        if response.json().get('is_ai_turn'):
            pawns_response = requests.get(f'http://localhost:5000/get_player_pawns/{player_index}')
            pawns = pawns_response.json().get('pawns')

            if pawns:
                pawn = random.choice(pawns)  # Choose a random pawn to move
                moves_response = requests.get(f'http://localhost:5000/get_moves/{pawn[0]}/{pawn[1]}')
                moves = moves_response.json().get('moves')
                if moves:
                    current_position = pawn  # Save the current position of the pawn
                    best_move = choose_best_move(moves, goals, current_position)
                    target_x, target_y = best_move
                    move_response = requests.post(f'http://localhost:5000/move/{pawn[0]}/{pawn[1]}/{target_x}/{target_y}')
                    if move_response.status_code == 200:
                        print("Move successful.")
                    else:
                        print("Invalid move.")
                else:
                    print("No available moves for pawn.")
            else:
                print("No pawns available.")

        # wait for 1 second
        time.sleep(0.1)

    except requests.exceptions.RequestException as e:
        print(e)
