import pygame
import sys
import numpy
import sys

color_light = (202, 203, 213)
color_dark = (2, 6, 145)
y_scaling_factor = 1.5

# Neon colors:
class Colors:
    # Modified tones of existing colors
    RED = (255, 80, 80)       # Lighter red
    YELLOW = (255, 255, 102)  # Lighter yellow
    ORANGE = (255, 140, 0)    # Darker orange
    GREEN = (0, 200, 0)       # Darker green
    PURPLE = (178, 102, 255)  # Lighter purple
    BLUE = (0, 102, 204)      # Darker blue
    BLACK = (51, 51, 51)      # Modified black
    GREY = (160, 160, 160)
    WHITE = (240, 240, 240)   # Modified white

def SixPlayers(number_of_players):
    pygame.init()
    matrix = numpy.ones((17, 25)) * -1

    if number_of_players == 2:
        players_list = [
            [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]],
            [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
        ]
    elif number_of_players == 3:
        players_list = [
            [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]],
            [[12, 18], [12, 20], [12, 22], [12, 24], [11, 19], [11, 21], [11, 23], [10, 20], [10, 22], [9, 21]],
            [[12, 0], [12, 2], [12, 4], [12, 6], [11, 1], [11, 3], [11, 5], [10, 2], [10, 4], [9, 3]]
        ]
    elif number_of_players == 4:[
            [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]],
            [[12, 18], [12, 20], [12, 22], [12, 24], [11, 19], [11, 21], [11, 23], [10, 20], [10, 22], [9, 21]],
            [[12, 0], [12, 2], [12, 4], [12, 6], [11, 1], [11, 3], [11, 5], [10, 2], [10, 4], [9, 3]],
            [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]
    ]
    elif number_of_players == 6:
        players_list = [
            [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]],
            [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]],
            [[12, 18], [12, 20], [12, 22], [12, 24], [11, 19], [11, 21], [11, 23], [10, 20], [10, 22], [9, 21]],
            [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]],
            [[12, 0], [12, 2], [12, 4], [12, 6], [11, 1], [11, 3], [11, 5], [10, 2], [10, 4], [9, 3]],
            [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]
        ]
    else:
        print("Invalid number of players. Valid options are 2, 3, 4, or 6.")
        sys.exit(1)

    move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]
    matrix_index = [1, 2, 3, 4, 13, 12, 11, 10, 9]
    for i in range(9):
        j = 12
        first_time = True
        while matrix_index[i] > 0:
            if (i % 2 == 0) and first_time:
                first_time = False
                matrix[i][j] = matrix[16 - i][j] = 0
                matrix_index[i] -= 1
            else:
                j -= 1
                matrix[i][j] = matrix[i][24 - j] = matrix[16 - i][j] = matrix[16 - i][24 - j] = 0
                matrix_index[i] -= 2
            j -= 1

    index = 1
    for player in players_list[:number_of_players]:
        for i in range(len(player)):
            matrix[player[i][0]][player[i][1]] = index
        index += 1

    print(np.matrix(matrix))

    def draw_pawns():
        colors = [Colors.GREY, Colors.RED, Colors.YELLOW, Colors.ORANGE, Colors.GREEN, Colors.PURPLE, Colors.BLUE]
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(
                        j * CELL_SIZE, i * CELL_SIZE * y_scaling_factor, CELL_SIZE, CELL_SIZE
                    )
                    pawns_rect.append(
                        pygame.draw.rect(
                            screen,
                            colors[int(matrix[i][j])],
                            rect,
                            border_radius=20,
                        )
                    )

    def get_valid_moves(coor):
        valid_index = []
        for i in range(len(move_index)):

            x = coor[0] + move_index[i][0]
            y = coor[1] + move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif matrix[x][y] != -1:
                    check_path(move_index[i], x, y, valid_index)

        return valid_index

    def check_path(path_coor, x, y, moves_array):
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(move_index)):
                        x3 = x2 + move_index[j][0]
                        y3 = y2 + move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
                                if matrix[x3][y3] > 0:
                                    check_path(move_index[j], x3, y3, moves_array)

    def move(pos, target):
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

    def get_token_coor(x, y):
        grid_width = 0
        grid_heigth = 0
        coor = [int((y - grid_heigth) / (CELL_SIZE * y_scaling_factor)), int((x - grid_width) / CELL_SIZE)]
        return coor

    def add_selected_effect(moves=[], clicked_token=None):
        colors = [Colors.GREY, Colors.RED, Colors.YELLOW, Colors.ORANGE, Colors.GREEN, Colors.PURPLE, Colors.BLUE]
        moves.append(clicked_token)
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(
                        j * CELL_SIZE, i * CELL_SIZE * y_scaling_factor, CELL_SIZE, CELL_SIZE
                    )
                    pawns_rect.append(
                        pygame.draw.rect(
                            screen, colors[int(matrix[i][j])], rect, border_radius=CELL_SIZE
                        )
                    )
                if [i, j] in moves:
                    test_cercle = pygame.image.load("imgs/cercle.png")
                    test_cercle = pygame.transform.scale(
                        test_cercle, (CELL_SIZE, CELL_SIZE)
                    )
                    screen.blit(test_cercle, (j * CELL_SIZE, i * CELL_SIZE * y_scaling_factor))

    def write_text(text, text_pos_x, text_pos_y, text_size, col):
        text_font = pygame.font.SysFont(None, text_size)
        text_render = text_font.render(text, True, col)
        screen.blit(text_render, (text_pos_x, text_pos_y))

    def check_winner():
        #TODO: Implement the winner function
        return False
    
    def get_player_pawns(player_index):
        pawns = []
        for i in range(17):
            for j in range(25):
                if matrix[i][j] == player_index:
                    pawns.append([i, j])
        return pawns

    def get_all_possible_player_moves(player_index):
        moves = []
        for i in range(17):
            for j in range(25):
                if matrix[i][j] == player_index:
                    moves += get_valid_moves([i, j])
        return moves

    num_columns = 25
    num_rows = 25
    CELL_SIZE = 20
    screen = pygame.display.set_mode(size=(num_columns * CELL_SIZE, num_rows * CELL_SIZE + 100))
    timer = pygame.time.Clock()
    game_on = True
    pawns_rect = []

    screen.fill(pygame.Color(Colors.BLACK))
    draw_pawns()
    player_index = 1
    player_valid_moves = []
    last_selected_token = []

    player_colours = [Colors.RED, Colors.YELLOW, Colors.ORANGE, Colors.GREEN, Colors.PURPLE, Colors.BLUE]

    while game_on:
        col = player_colours[player_index - 1]

        write_text(
            "Player " + str(player_index) + "'s Turn",
            num_columns * CELL_SIZE - 370,
            num_rows * CELL_SIZE + 30,
            50,
            col,
        )

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # get a list of all sprites that are under the mouse cursor
            clicked_sprites = [s for s in pawns_rect if s.collidepoint(pos)]

            if clicked_sprites:
                clicked_token = get_token_coor(
                    clicked_sprites[0].x, clicked_sprites[0].y
                )
                if matrix[clicked_token[0], clicked_token[1]] == player_index:
                    if clicked_token == last_selected_token:
                        last_selected_token = []
                        player_valid_moves = []
                    else:
                        player_valid_moves = get_valid_moves(clicked_token)
                        last_selected_token = clicked_token
                    screen.fill(pygame.Color(Colors.BLACK))
                    add_selected_effect(player_valid_moves, last_selected_token)
                elif clicked_token in player_valid_moves:
                    move(last_selected_token, clicked_token)
                    check_winner()
                    last_selected_token = []
                    player_valid_moves = []
                    screen.fill(pygame.Color(Colors.BLACK))
                    player_index = (player_index + 1) % (number_of_players + 1)
                    if player_index == 0:
                        player_index += 1
                    add_selected_effect()

                game_on = not check_winner()
        pygame.display.update()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Default number of players is 2. If you want to change it, please provide a valid integer as an argument."
        )
        number_of_players = 2
    else:
        try:
            number_of_players = int(sys.argv[1])
        except ValueError:
            print("Invalid number of players. Please provide a valid integer.")
            sys.exit(1)

    SixPlayers(number_of_players)
