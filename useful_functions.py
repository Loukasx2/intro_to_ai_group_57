import yaml
import random

# Load config file
with open("config.yaml", "r") as yamlfile:
    cfg = yaml.safe_load(yamlfile)

BOARD_SIZE_X = cfg["board_size"]
BOARD_SIZE_Y = BOARD_SIZE_X
NUMBER_OF_ROWS_WITH_PAWNS = cfg["number_of_rows_with_pawns"]

class UsefulFunctions:
    def __init__(self):
        self.move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]
    
    def get_valid_moves(self, matrix, coor):
        valid_index = []
        for i in range(len(self.move_index)):

            x = coor[0] + self.move_index[i][0]
            y = coor[1] + self.move_index[i][1]
            if -1 < x < BOARD_SIZE_X and -1 < y < BOARD_SIZE_Y:
                if matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif matrix[x][y] != -1:
                    valid_index = self.check_path(matrix, self.move_index[i], x, y, valid_index)
        random.shuffle(valid_index)
        return valid_index

    def check_path(self, matrix, path_coor, x, y, moves_array):
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < BOARD_SIZE_X and -1 < y2 < BOARD_SIZE_Y:
                if matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(self.move_index)):
                        x3 = x2 + self.move_index[j][0]
                        y3 = y2 + self.move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < BOARD_SIZE_X and -1 < y3 < BOARD_SIZE_Y:
                                if matrix[x3][y3] > 0:
                                    self.check_path(matrix, self.move_index[j], x3, y3, moves_array)
        return moves_array
    
    def move(self, matrix, pos, target):
        # if self.player_index != matrix[pos[0]][pos[1]]:
        #     print(f"Invalid move. Not your turn. Player {self.player_index} is playing and you are trying to move player {matrix[pos[0]][pos[1]]}'s pawn.")
        #     return False
        valid_moves = self.get_valid_moves(matrix, pos)
        if target not in valid_moves:
            print("Invalid move. Target not in valid moves.")
            print(f"Tried to move from {pos} to {target}. Valid moves are {valid_moves}")
            return False
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

        return matrix
    
    def get_pawns(self, matrix, player_index):
        pawns = []
        for i in range(BOARD_SIZE_X):
            for j in range(BOARD_SIZE_Y):
                if matrix[i][j] == player_index:
                    pawns.append([i, j])
        random.shuffle(pawns)
        return pawns
    
    def get_starting_positions(self):
        i = 1
        player_1 = []
        player_2 = []
        middle_column = int(BOARD_SIZE_X / 2)
        player_1.append([0, middle_column])
        player_2.append([BOARD_SIZE_X - 1, middle_column])
        for j in range(1, NUMBER_OF_ROWS_WITH_PAWNS):
            for k in range(middle_column - i, middle_column + i + 1, 2):
                player_1.append([j, k])
                player_2.append([BOARD_SIZE_X - 1 - j, k])

            i += 1

        return player_1, player_2