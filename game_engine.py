import pygame
import sys
import numpy
import sys
import threading
import flask
import logging

color_light = (202, 203, 213)
color_dark = (2, 6, 145)
y_scaling_factor = 1.5
num_columns = 25
num_rows = 25
CELL_SIZE = 20

# Neon colors:
class Colors:
    # Modified tones of existing colors
    RED = (255, 80, 80)       # Lighter red
    YELLOW = (255, 255, 102)  # Lighter yellow
    ORANGE = (255, 140, 0)    # Darker orange
    GREEN = (0, 200, 0)       # Darker green
    PURPLE = (218, 102, 255)  # Lighter purple
    BLUE = (0, 102, 204)      # Darker blue
    BLACK = (51, 51, 51)      # Modified black
    GREY = (125, 125, 125)
    WHITE = (240, 240, 240)   # Modified white

class GameEngine():
    def __init__(self, number_of_players):
        pygame.init()
        self.matrix = numpy.ones((17, 25)) * -1
        self.number_of_players = number_of_players
        self.ai_player_numbers = [2, 3, 4, 5, 6]

        if number_of_players == 2:
            self.players_list = [
                [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]],
                [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
            ]
        elif number_of_players == 3:
            self.players_list = [
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
            self.players_list = [
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

        self.move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]
        matrix_index = [1, 2, 3, 4, 13, 12, 11, 10, 9]
        for i in range(9):
            j = 12
            first_time = True
            while matrix_index[i] > 0:
                if (i % 2 == 0) and first_time:
                    first_time = False
                    self.matrix[i][j] = self.matrix[16 - i][j] = 0
                    matrix_index[i] -= 1
                else:
                    j -= 1
                    self.matrix[i][j] = self.matrix[i][24 - j] = self.matrix[16 - i][j] = self.matrix[16 - i][24 - j] = 0
                    matrix_index[i] -= 2
                j -= 1

        index = 1
        for player in self.players_list[:number_of_players]:
            for i in range(len(player)):
                self.matrix[player[i][0]][player[i][1]] = index
            index += 1

    def draw_pawns(self,):
        colors = [Colors.GREY, Colors.RED, Colors.YELLOW, Colors.ORANGE, Colors.GREEN, Colors.PURPLE, Colors.BLUE]
        for i in range(0, 17):
            for j in range(0, 25):
                if self.matrix[i][j] >= 0:
                    if self.matrix[i][j] == 0:
                        circle_center = (j * CELL_SIZE + CELL_SIZE/2, i * CELL_SIZE * y_scaling_factor + CELL_SIZE/2)
                        circle_radius = CELL_SIZE/4
                    else:
                        circle_center = (j * CELL_SIZE + CELL_SIZE/2, i * CELL_SIZE * y_scaling_factor + CELL_SIZE/2)
                        circle_radius = CELL_SIZE/2
                    self.pawns_rect.append(
                        pygame.draw.circle(
                            self.screen, colors[int(self.matrix[i][j])], circle_center, circle_radius,
                        )
                    )

    def get_valid_moves(self,coor):
        valid_index = []
        for i in range(len(self.move_index)):

            x = coor[0] + self.move_index[i][0]
            y = coor[1] + self.move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if self.matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif self.matrix[x][y] != -1:
                    self.check_path(self.move_index[i], x, y, valid_index)

        return valid_index

    def check_path(self,path_coor, x, y, moves_array):
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if self.matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(self.move_index)):
                        x3 = x2 + self.move_index[j][0]
                        y3 = y2 + self.move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
                                if self.matrix[x3][y3] > 0:
                                    self.check_path(self.move_index[j], x3, y3, moves_array)

    def move(self, pos, target, ai_move=False):
        if self.player_index != self.matrix[pos[0]][pos[1]]:
            print(f"Invalid move. Not your turn. Player {self.player_index} is playing and you are trying to move player {self.matrix[pos[0]][pos[1]]}'s pawn.")
            return False
        valid_moves = self.get_valid_moves(pos)
        if target not in valid_moves:
            print("Invalid move. Target not in valid moves.")
            return False
        self.matrix[target[0]][target[1]] = self.matrix[pos[0]][pos[1]]
        self.matrix[pos[0]][pos[1]] = 0

        if ai_move:
            self.player_index = (self.player_index + 1) % (self.number_of_players + 1)
            if self.player_index == 0:
                self.player_index += 1
            # post event to update the game
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {}))

        return True

    def get_token_coor(self,x, y):
        grid_width = 0
        grid_heigth = 0
        coor = [int((y - grid_heigth) / (CELL_SIZE * y_scaling_factor)), int((x - grid_width) / CELL_SIZE)]
        return coor

    def add_selected_effect(self,moves=[], clicked_token=None):
        colors = [Colors.GREY, Colors.RED, Colors.YELLOW, Colors.ORANGE, Colors.GREEN, Colors.PURPLE, Colors.BLUE]
        moves.append(clicked_token)
        for i in range(0, 17):
            for j in range(0, 25):
                if self.matrix[i][j] >= 0:
                    if self.matrix[i][j] == 0:
                        circle_center = (int(j * CELL_SIZE + CELL_SIZE/2), int(i * CELL_SIZE * y_scaling_factor + CELL_SIZE/2))
                        circle_radius = int(CELL_SIZE/4)
                    else:
                        circle_center = (int(j * CELL_SIZE + CELL_SIZE/2), int(i * CELL_SIZE * y_scaling_factor + CELL_SIZE/2))
                        circle_radius = int(CELL_SIZE/2)
                    self.pawns_rect.append(
                        pygame.draw.circle(
                            self.screen, colors[int(self.matrix[i][j])], circle_center, circle_radius,
                        )
                    )
                if [i, j] in moves:
                    test_cercle = pygame.image.load("imgs/cercle.png")
                    test_cercle = pygame.transform.scale(
                        test_cercle, (CELL_SIZE, CELL_SIZE)
                    )
                    self.screen.blit(test_cercle, (j * CELL_SIZE, i * CELL_SIZE * y_scaling_factor))

    def write_text(self,text, text_pos_x, text_pos_y, text_size, col):
        text_font = pygame.font.SysFont(None, text_size)
        text_render = text_font.render(text, True, col)
        self.screen.blit(text_render, (text_pos_x, text_pos_y))

    def check_winner(self):
        #TODO: Implement the winner function
        for index, goal in enumerate(self.players_list):
            number_of_occupied_positions = 0
            number_of_self_occupied_positions = 0
            for i in range(len(goal)):
                if self.matrix[goal[i][0]][goal[i][1]] > 0:
                    number_of_occupied_positions += 1
                    if self.matrix[goal[i][0]][goal[i][1]] == index + 1:
                        number_of_self_occupied_positions += 1
            print(f"Number of occupied positions: {number_of_occupied_positions}")
            print(f"Number of self occupied positions: {number_of_self_occupied_positions}")
            if number_of_occupied_positions == len(goal) and number_of_self_occupied_positions != len(goal):
                return True
        return False
    
    def get_player_pawns(self,player_index):
        pawns = []
        for i in range(17):
            for j in range(25):
                if self.matrix[i][j] == player_index:
                    pawns.append([i, j])
        return pawns

    def get_all_possible_player_moves(self,player_index):
        moves = []
        for i in range(17):
            for j in range(25):
                if self.matrix[i][j] == player_index:
                    moves += self.get_valid_moves([i, j])
        return moves
    
    def is_ai_turn(self, player_index):
        return player_index == self.player_index
    
    def run(self):
        self.screen = pygame.display.set_mode(size=(num_columns * CELL_SIZE, num_rows * CELL_SIZE + 100))
        game_on = True
        self.pawns_rect = []

        self.screen.fill(pygame.Color(Colors.BLACK))
        time = pygame.time.Clock()
        self.draw_pawns()
        self.player_index = 1
        player_valid_moves = []
        last_selected_token = []

        player_colours = [Colors.RED, Colors.YELLOW, Colors.ORANGE, Colors.GREEN, Colors.PURPLE, Colors.BLUE]

        while game_on:
            col = player_colours[self.player_index - 1]

            self.write_text(
                "Player " + str(self.player_index) + "'s Turn",
                num_columns * CELL_SIZE - 370,
                num_rows * CELL_SIZE + 30,
                50,
                col,
            )

            if self.player_index in self.ai_player_numbers:
                event = pygame.event.wait()
                self.screen.fill(pygame.Color(Colors.BLACK))
                self.add_selected_effect()
                game_on = not self.check_winner()
            else:
                pygame.display.update()
                event = pygame.event.wait()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # get a list of all sprites that are under the mouse cursor
                    clicked_sprites = [s for s in self.pawns_rect if s.collidepoint(pos)]

                    if clicked_sprites:
                        clicked_token = self.get_token_coor(
                            clicked_sprites[0].x, clicked_sprites[0].y
                        )
                        if self.matrix[clicked_token[0], clicked_token[1]] == self.player_index:
                            if clicked_token == last_selected_token:
                                last_selected_token = []
                                player_valid_moves = []
                            else:
                                player_valid_moves = self.get_valid_moves(clicked_token)
                                last_selected_token = clicked_token
                            self.screen.fill(pygame.Color(Colors.BLACK))
                            self.add_selected_effect(player_valid_moves, last_selected_token)
                        elif clicked_token in player_valid_moves:
                            self.move(last_selected_token, clicked_token)
                            self.check_winner()
                            last_selected_token = []
                            player_valid_moves = []
                            self.screen.fill(pygame.Color(Colors.BLACK))
                            self.player_index = (self.player_index + 1) % (self.number_of_players + 1)
                            if self.player_index == 0:
                                self.player_index += 1
                            self.add_selected_effect()

                        game_on = not self.check_winner()
            pygame.display.update()

        self.write_text(
            "We have a winner!",
            num_columns * CELL_SIZE - 370,
            num_rows * CELL_SIZE + 30,
            50,
            Colors.WHITE,
        )
        pygame.display.update()
        time.tick(60 * 250) 

    def __del__(self):
        print("Game ended.")
        pygame.quit()

if __name__ == "__main__":
    print("Welcome to the game of Chinese Checkers!")
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

    game = GameEngine(number_of_players)
    # run game in thread
    game_thread = threading.Thread(target=game.run)
    game_thread.daemon = True
    game_thread.start()
    print("Game is running...")

    # create an API to interact with the game
    app = flask.Flask(__name__)
    logging.getLogger('werkzeug').disabled = True

    @app.route("/get_player_pawns/<int:player_index>", methods=["GET"])
    def get_player_pawns(player_index):
        return {"pawns": game.get_player_pawns(player_index)}
    
    @app.route("/get_all_possible_player_moves/<int:player_index>", methods=["GET"])
    def get_all_possible_player_moves(player_index):
        return {"moves": game.get_all_possible_player_moves(player_index)}
    
    @app.route("/get_moves/<int:pos_x>/<int:pos_y>", methods=["GET"])
    def get_moves(pos_x, pos_y):
        return {"moves": game.get_valid_moves([pos_x, pos_y])}
    
    @app.route("/is_ai_turn/<int:player_index>", methods=["GET"])
    def is_ai_turn(player_index):
        return {"is_ai_turn": game.is_ai_turn(player_index)}
    
    @app.route("/move/<int:pos_x>/<int:pos_y>/<int:target_x>/<int:target_y>", methods=["POST"])
    def move(pos_x, pos_y, target_x, target_y):
        res = game.move([pos_x, pos_y], [target_x, target_y], ai_move=True)
        if not res:
            # answer with an error code
            return {"message": "Invalid move."}, 400
        return {"message": "Move successful."}
    
    app.run(port=5000)