
class UsefulFunctions:
    def __init__(self):
        self.move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]
    
    def get_valid_moves(self, matrix, coor):
        valid_index = []
        for i in range(len(self.move_index)):

            x = coor[0] + self.move_index[i][0]
            y = coor[1] + self.move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif matrix[x][y] != -1:
                    valid_index = self.check_path(matrix, self.move_index[i], x, y, valid_index)
        return valid_index

    def check_path(self, matrix, path_coor, x, y, moves_array):
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(self.move_index)):
                        x3 = x2 + self.move_index[j][0]
                        y3 = y2 + self.move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
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
        for i in range(17):
            for j in range(25):
                if matrix[i][j] == player_index:
                    pawns.append([i, j])
        return pawns