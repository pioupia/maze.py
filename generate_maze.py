import random
from typing import List, Tuple

# Génère un labyrinthe suivant les règles (Prim's):
# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm

# Types
GameMap = List[List[str]]
Box = List[int]

BIT_MAP = [[1, 0], [-1, 0], [0, 1], [0, -1]]

# On définit les caractères dans notre tableau
wall_char = '#'
cell_char = '.'
unvisited_char = 'u'


def surrounding_cells(maze: GameMap, rand_wall: Box) -> Tuple[GameMap, int]:
    """
    Permet de calculer le nombre de cellules voisines à une cellule

    :param maze: GameMap
    :param rand_wall: Box
    :return: Tuple[GameMap, int]
    """
    s_cells = 0

    for neigh in BIT_MAP:
        if maze[rand_wall[0] + neigh[0]][rand_wall[1] + neigh[1]] == cell_char:
            s_cells += 1

    return maze, s_cells


def generate_maze(width: int, height: int) -> GameMap:
    """
    Permet de générer un labyrinthe
    :param width: int - Largeur du labyrinthe
    :param height: int - Hauteur du labyrinthe
    :return: GameMap
    """
    maze = []

    # On définit toutes les cellules comme non visitées
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited_char)
        maze.append(line)

    # On assigne un point de départ aléatoirement comme cellule
    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)

    # On s'assure qu'on n'est pas au bord du labyrinthe
    if starting_height == 0:
        starting_height += 1
    elif starting_height == height - 1:
        starting_height -= 1

    if starting_width == 0:
        starting_width += 1
    elif starting_width == width - 1:
        starting_width -= 1

    # On définit dans le labyrinthe la cellule comme "cellule"
    maze[starting_height][starting_width] = cell_char

    # On définit un tableau pour les murs, et on y met tous les voisins
    # de la cellule fraichement instanciée.
    walls = [
        # Mur du dessus
        [starting_height - 1, starting_width],

        # Mur à gauche
        [starting_height, starting_width - 1],

        # Mur à droite
        [starting_height, starting_width + 1],

        # Mur en dessous
        [starting_height + 1, starting_width]
    ]

    # On définit nos murs fraichement ajoutés à notre tableau
    # en tant que "mur" dans notre labyrinthe
    maze[starting_height - 1][starting_width] = wall_char
    maze[starting_height][starting_width - 1] = wall_char
    maze[starting_height][starting_width + 1] = wall_char
    maze[starting_height + 1][starting_width] = wall_char

    # Tant qu'il nous reste des murs
    while walls:
        # On choisit un mur aléatoire de la liste des murs.
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        for neighbor in BIT_MAP:
            x = rand_wall[1] + neighbor[1]
            y = rand_wall[0] + neighbor[0]

            x_opposite = rand_wall[1] - neighbor[1]
            y_opposite = rand_wall[0] - neighbor[0]

            # Si la case est trop à gauche ou trop à droite, on évite de faire les calculs
            # on risque de sortie du tableau
            if neighbor[0] == 0 and (rand_wall[1] == 0 or rand_wall[1] == width - 1):
                continue
            # Et si la case est trop en haut ou trop en bas, on évite de faire les calculs.
            elif neighbor[1] == 0 and (rand_wall[0] == 0 or rand_wall[0] == height - 1):
                continue

            # On vérifie que les cases voisines (droite/gauche ou haut/bas)
            # soient pour l'une non visitée, et pour l'autre une cellule
            if (maze[y][x] == unvisited_char
                    and maze[y_opposite][x_opposite] == cell_char):

                # On vérifie qu'il y ait au maximum une cellule voisine
                maze, s_cells = surrounding_cells(maze, rand_wall)

                if s_cells > 2:
                    continue

                # On "casse le mur", et on le définit en tant que cellule
                maze[rand_wall[0]][rand_wall[1]] = cell_char

                # On va marquer les nouveaux murs

                # Case du dessus (on s'assure que ce n'est pas le bord haut)
                if rand_wall[0] != 0:
                    # Si jamais la case du dessus n'est pas une cellule
                    if maze[rand_wall[0] - 1][rand_wall[1]] != cell_char:
                        # Alors on la définit comme un mur
                        maze[rand_wall[0] - 1][rand_wall[1]] = wall_char

                    # Et si jamais elle n'est pas instanciée dans nos murs
                    if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                        # Alors on l'ajoute
                        walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Case en dessous
                if rand_wall[0] != height - 1:
                    if maze[rand_wall[0] + 1][rand_wall[1]] != cell_char:
                        maze[rand_wall[0] + 1][rand_wall[1]] = wall_char
                    if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                        walls.append([rand_wall[0] + 1, rand_wall[1]])

                # Case de gauche
                if rand_wall[1] != 0:
                    if maze[rand_wall[0]][rand_wall[1] - 1] != cell_char:
                        maze[rand_wall[0]][rand_wall[1] - 1] = wall_char
                    if [rand_wall[0], rand_wall[1] - 1] not in walls:
                        walls.append([rand_wall[0], rand_wall[1] - 1])

                # Case à droite
                if rand_wall[1] != width - 1:
                    if maze[rand_wall[0]][rand_wall[1] + 1] != cell_char:
                        maze[rand_wall[0]][rand_wall[1] + 1] = wall_char
                    if [rand_wall[0], rand_wall[1] + 1] not in walls:
                        walls.append([rand_wall[0], rand_wall[1] + 1])

            # On retire ce mur de la liste des murs
            for wall in walls:
                # En s'assurant qu'il en fait bien parti
                if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                    walls.remove(wall)

            continue

    walls = []

    # On définit toutes les dernières cellules "non visitées" comme des murs.
    # Et on ajoute à notre tableau des murs, tous les murs restant
    for i in range(height):
        for j in range(width):
            if maze[i][j] == unvisited_char:
                maze[i][j] = wall_char

            # On vérifie que c'est un mur, et pas un mur du contour
            if maze[i][j] == wall_char and i != 0 and j != 0 and j != height - 1 and i != width - 1:
                walls.append((j, i))

    # On parcourt 10% des murs afin de les retirer (permet de créer plusieurs chemins possibles)
    walls_count = len(walls) // 10
    for i in range(walls_count):
        # On tire un mur au hasard
        wall = random.choice(walls)

        # Et on le remplace par une cellule (Oui, certain mur pourront déjà avoir été tiré au sort
        # Mais cela ajoute plus "d'aléatoire" à la génération du labyrinthe).
        maze[wall[1]][wall[0]] = cell_char


    maze[0][0] = 'e'
    maze[-1][-1] = 's'

    # Définir la sortie et l'entrée
    maze[0][0] = 'e'
    maze[0][1] = '.'
    maze[-1][-1] = 's'

    # Si jamais le point de sortie est isolé (ça arrive parfois)
    if maze[-1][-2] != '.' and maze[-2][-1] != '.':
        # On regarde les voisins pour faire sauter soit le mur au dessus, soit le mur à droite
        # En fonction des valeurs voisines.
        if maze[-1][-3] == '.':
            maze[-1][-2] = '.'
        else:
            maze[-2][-1] = '.'

    return maze
