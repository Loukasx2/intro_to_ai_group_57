import pygame
import sys
import numpy
import sys

color_light = (202, 203, 213 )
color_dark = (2, 6, 145)
def SixPlayers(number_of_players):
    pygame.init()
    # remplir la matrice avec des 1
    matrix = numpy.ones((17, 25))
    # remplir la matrice avec des -1
    matrix *= -1


    # les positions des pions dans la matrice pour chaque joueur
    players_list = [
        [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]],   #red
        [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]],    #yellow
        [[12, 18], [12, 20], [12, 22], [12, 24], [11, 19], [11, 21], [11, 23], [10, 20], [10, 22], [9, 21]], #orange
        [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]], #green
        [[12, 0], [12, 2], [12, 4], [12, 6], [11, 1], [11, 3], [11, 5], [10, 2], [10, 4], [9, 3]],   #purple
        [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]   #blue
    ]
    move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]
    #modification de la matrice
    #changer des -1 par des 0 pour les cases de l'etoile
    matrix_index = [1, 2, 3, 4, 13, 12, 11, 10, 9]
    for i in range(9):
        j = 12
        first_time = True
        while matrix_index[i] > 0:
            if (i % 2 == 0) and first_time:
                first_time = False
                # print(i,j)
                matrix[i][j] = matrix[16 - i][j] = 0

                matrix_index[i] -= 1
            else:
                j -= 1
                matrix[i][j] = matrix[i][24 - j] = matrix[16 - i][j] = matrix[16 - i][24 - j] = 0
                matrix_index[i] -= 2
            j -= 1

    #modification matrice : 1 pour joueur numero 1 ,2 pour joueur numero 2....
    def add_players():
        index = 1
        for player in players_list[:number_of_players]:
            for i in range(len(player)):
                matrix[player[i][0]][player[i][1]] = index
            index += 1

    class remplissage:
        def __init__(self):
            self_x = 0
            self_y = 0

        def pion(self):
            colors = ["grey", "red", "yellow", "orange", "green", "purple", "blue"]
            for i in range(0, 17):
                for j in range(0, 25):
                    if matrix[i][j] >= 0:
                        rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pions_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))

    #les pas possibles
    def valid_moves(coor):
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
    #les sauts possibles
    def check_path(path_coor, x, y, moves_array):
        # print('before:', x, y)
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

    #pour faire le mouvement
    def move(pos, target):
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

        # les coordonnees parraport a la grille
    def get_token_coor(x, y):
            grid_width = 0
            grid_heigth = 0
            coor = [int((y - grid_heigth) / 20), int((x - grid_width) / 20)]
            return coor
        # l'animation des deplasssements possibles


    def animation(moves=[], clicked_token=None):
        colors = ["grey", "red", "yellow", "orange", "green", "purple", "blue"]
        moves.append(clicked_token)
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pions_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))
                if [i, j] in moves:
                    test_cercle = pygame.image.load('imgs/cercle.png')
                    test_cercle = pygame.transform.scale(test_cercle, (CELL_SIZE, CELL_SIZE))
                    screen.blit(test_cercle, (j * CELL_SIZE, i * CELL_SIZE))

        # grille
    def show_grille():
            for i in range(0, nb_col):
                for j in range(0, nb_ligne):
                    rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, pygame.Color("white"), rect, width=1)

        # fonction pour ajouter un text a l'ecran
    def WriteText(text, text_pos_x, text_pos_y, text_size, col):
            text_font = pygame.font.SysFont(None, text_size)
            text_render = text_font.render(text, True, col)
            screen.blit(text_render, (text_pos_x, text_pos_y))


    # afficher le gagnant
    def winner():
        return False

    add_players()
    # l'affichage de la fenetre du jeu
    nb_col = 25
    nb_ligne = 25
    CELL_SIZE = 20
    screen = pygame.display.set_mode(size=(nb_col * CELL_SIZE, nb_ligne * CELL_SIZE))
    timer = pygame.time.Clock()
    game_on = True
    pions_rect = []


    players = remplissage()


    screen.fill(pygame.Color("white"))
    players.pion()
    player_index = 1
    is_selecting = False
    player_valid_moves = []
    last_selected_token = []
    #fonction boutton pour le retour a la fenetre precedente

    def text_objects(text, font):
        textsurface = font.render(text, True, "white")
        return textsurface, textsurface.get_rect()

    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)
    while game_on:
        # player turn
        if player_index == 1: col = 'red'
        if player_index == 2: col = 'yellow'
        if player_index == 3: col = 'orange'
        if player_index == 4: col = 'green'
        if player_index == 5: col = 'purple'
        if player_index == 6: col = 'blue'
        # player turn
        if (winner() == False):
            WriteText('Player ' + str(player_index) + '\'s Turn', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100,
                      50, col)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in pions_rect if s.collidepoint(pos)]

                if clicked_sprites:
                    clicked_token = get_token_coor(clicked_sprites[0].x, clicked_sprites[0].y)
                    if matrix[clicked_token[0], clicked_token[1]] == player_index:
                        if clicked_token == last_selected_token:
                            is_selecting = False
                            last_selected_token = []
                            player_valid_moves = []
                            screen.fill(pygame.Color("white"))
                            animation()
                        else:
                            player_valid_moves = valid_moves(clicked_token)
                            last_selected_token = clicked_token
                            is_selecting = True
                            screen.fill(pygame.Color("white"))
                            animation(player_valid_moves,last_selected_token)
                    elif clicked_token in player_valid_moves:
                        move(last_selected_token, clicked_token)
                        winner()
                        is_selecting = False
                        last_selected_token = []
                        player_valid_moves = []
                        screen.fill(pygame.Color("white"))
                        player_index = (player_index+1) % (number_of_players+1)
                        if player_index == 0:
                            player_index += 1


                        animation()
        pygame.display.update()
        timer.tick(60)

if len(sys.argv) < 2:
    print("Default number of players is 2. If you want to change it, please provide a valid integer as an argument.")
    number_of_players = 2
else:
    try:
        number_of_players = int(sys.argv[1])
    except ValueError:
        print("Invalid number of players. Please provide a valid integer.")
        sys.exit(1)

SixPlayers(number_of_players)