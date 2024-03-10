import requests
import random
import time
import sys

# get the player index from command line arguments
player_index = int(sys.argv[1])

while True:
    try:
        response = requests.get(f'http://localhost:5000/is_ai_turn/{player_index}')
        if response.json().get('is_ai_turn'):
            # player_index = 2  # Replace with the desired player index
            while True:
                pawns_response = requests.get(f'http://localhost:5000/get_player_pawns/{player_index}')
                pawns = pawns_response.json().get('pawns')
                random_pawn = random.choice(pawns)
                pos_x, pos_y = random_pawn
                moves_response = requests.get(f'http://localhost:5000/get_moves/{pos_x}/{pos_y}')
                if len(moves_response.json().get('moves')) > 0:
                    break
            random_move = random.choice(moves_response.json().get('moves'))
            target_x, target_y = random_move
            move_response = requests.post(f'http://localhost:5000/move/{pos_x}/{pos_y}/{target_x}/{target_y}')
            if move_response.status_code == 200:
                print("Move successful.")
            else:
                print("Invalid move.")
        # wait for 1 second
    except requests.exceptions.RequestException as e:
        print(e)
    # time.sleep(0.25)