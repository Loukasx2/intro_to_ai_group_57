# intro_to_ai_group_57

Public repository for the group project in Introduction to AI course to implement an AI to play Chinese Checkers.

## Code structure

The code is composed of three main files:

- game_engine.py: Contains the game engine, which is responsible for running the game and keeping track of the game state.
- AI.py: Contains the AI, which is responsible for making moves for a player.
- useful_functions.py: Contains a set of useful functions that are used by both the game engine and the AI. Even though the AI is not allowed to use the game engine, it is allowed to use the useful functions, as it contains just a way to check the possible moves and being able to generate new board states based on the moves, which is necessary for the AI to work.

The only interaction between the game engine and the AI is made through an API, which is defined in the game engine file. The AI is not allowed to access the game engine directly, and the game engine is not allowed to access the AI directly. The available endpoints are:

- GET /is_ai_turn: Returns True if it is the AI's turn to play, and False otherwise.
- GET /get_board: Returns the current board state.
- POST /move/<int:pos_x>/<int:pos_y>/<int:target_x>/<int:target_y>: Makes a move from (pos_x, pos_y) to (target_x, target_y).

## Running the code

The code is written in Python 3. There's a requirements.txt file that contains the necessary dependencies to run the code. To install the dependencies, run:

```
pip install -r requirements.txt
```

The file config.yaml contains configuration for the game and the AI. The following parameters are available:

- is_player_one_bot: If true, player one will be controlled by the AI. If false, player one will be controlled by a human.
- is_player_two_bot: If true, player two will be controlled by the AI. If false, player two will be controlled by a human.
- depth: The depth of the search tree for the AI. The higher the depth, the more time it will take to make a move.
- board_size: The size of the board. Must be an odd number.
- number_of_rows_with_pawns: The number of rows with pawns for each player.
- alpha_beta_pruning: If true, the AI will use alpha-beta pruning to optimize the search tree.

To run the game engine:

```
python game_engine.py
```

A window will open, and you will be able to play the game. Click on the piece you want to move, and then click on the target position. If the AI is playing, it will make a move automatically.

To run the AI:

```
python AI.py $player_number
```

With player_number indicating which player the random player is.

Each command need to be run in a different terminal.
