# intro_to_ai_group_57

This project implements an AI for Chinese Checkers.

Our group repository can be found here [Group 57](https://github.com/Loukasx2/intro_to_ai_group_57).

# Code Structure

The codebase consists of three essential Python files:

1. **game_engine.py**: This file acts as the game's core, managing the board state, game logic, and graphical interface (if applicable). It is an adaptation of the repository [Chinese-Checkers](https://github.com/nourelhouda-taroudi/Chinese-checkers).
2. **AI.py**: This file houses the AI, responsible for analyzing the current board state and strategically selecting moves for its assigned player.
3. **useful_functions.py**: This file contains helper functions utilized by both the game engine and AI. These functions provide essential functionalities like validating moves and simulating potential board states based on moves, crucial for the AI's decision-making process.

**Encapsulation for Robustness:**

**Crucially, the game engine and AI are strictly isolated to prevent unintended interactions.** They communicate solely through a well-defined API established within `game_engine.py`. This API offers controlled access to specific functionalities:

- **GET /is_ai_turn:** Confirms if it's the AI's turn (True) or not (False).
- **GET /get_board:** Retrieves the current game state of the board.
- **POST /move/<int:pos_x>/<int:pos_y>/<int:target_x>/<int:target_y>**: Executes a move from starting position (`pos_x`, `pos_y`) to the target position (`target_x`, `target_y`).

**Important Note:**

_The `useful_functions.py` file, while accessible to both the engine and AI, serves purely as a collection of helper functions._ There's **no direct exchange of information or decision-making logic** between the engine and AI through this file.

### Running the Project

**Important Note:** This project has been tested successfully only on Linux/Ubuntu and Windows environments and is known to have issues on Macs.

This project is written in Python 3. Dependencies required to run the code are listed in a file named `requirements.txt`. You can install them using the following command:

```

pip install -r requirements.txt

```

A configuration file named `config.yaml` allows you to customize game and AI settings:

- **is_player_one_bot:** Set to `True` if Player 1 is controlled by the AI, `False` for human control.
- **is_player_two_bot:** Set to `True` if Player 2 is controlled by the AI, `False` for human control.
- **depth:** Defines the depth of the AI's search tree. Higher values result in more analysis time but potentially better moves.
- **board_size:** Sets the size of the game board (must be an odd number).
- **number_of_rows_with_pawns:** Specifies the number of starting pawn rows for each player.
- **alpha_beta_pruning:** Enables (`True`) or disables (`False`) alpha-beta pruning for search tree optimization.

**Launching the Game:**

To run the game engine with a graphical interface, execute:

```

python game_engine.py

```

This will open a window where you can click on pieces to move them. The AI will automatically make its moves if configured.

**Running the AI:**

To run the AI for a specific player (replace `$player_number` with the actual player number), use:

```

python AI.py $player_number

```

**Important Note:**

Run previous commands in separate terminal windows to ensure proper functionality.
