import requests
import random
import time
import sys

# get the player index from command line arguments
player_index = int(sys.argv[1])

goals = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]

while True:
    try:
        response = requests.get(f'http://localhost:5000/is_ai_turn/{player_index}')
        if response.json().get('is_ai_turn'):
            pawns_response = requests.get(f'http://localhost:5000/get_player_pawns/{player_index}')
            pawns = pawns_response.json().get('pawns')

            # implement algorithm here
            # get all possible moves and evaluate their score based on the distance to the goal
            # choose the move with the highest score
            # pawns = [[X, Y], [X, Y], ...
            # to get moves for a pawn, use the following endpoint:
            # moves_response = requests.get(f'http://localhost:5000/get_moves/{pos_x}/{pos_y}')
            # moves = moves_response.json().get('moves')
            # with moves being a list of [target_x, target_y] coordinates

            move_response = requests.post(f'http://localhost:5000/move/{pos_x}/{pos_y}/{target_x}/{target_y}')
            if move_response.status_code == 200:
                print("Move successful.")
            else:
                print("Invalid move.")
        # wait for 1 second
    except requests.exceptions.RequestException as e:
        print(e)
    time.sleep(0.25)