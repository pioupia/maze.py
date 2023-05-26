import random
from typing import List, Tuple

# Generate a maze following these rules (Prim's):
# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm

# Types
GameMap = List[List[str]]
Box = List[int]

BIT_MAP = [[1, 0], [-1, 0], [0, 1], [0, -1]]

# We define the characters in our list
wall_char = '#'
cell_char = '.'
unvisited_char = 'u'


def surrounding_cells(maze: GameMap, rand_wall: Box) -> Tuple[GameMap, int]:
    """
    Used to calculate the number of neighbouring cells to a cell

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
    Generates a maze

    :param width: int
    :param height: int
    :return: GameMap
    """
    maze = []

    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited_char)
        maze.append(line)

    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)

    if starting_height == 0:
        starting_height += 1
    elif starting_height == height - 1:
        starting_height -= 1

    if starting_width == 0:
        starting_width += 1
    elif starting_width == width - 1:
        starting_width -= 1

    maze[starting_height][starting_width] = cell_char

    walls = [
        [starting_height - 1, starting_width],
        [starting_height, starting_width - 1],
        [starting_height, starting_width + 1],
        [starting_height + 1, starting_width]
    ]

    maze[starting_height - 1][starting_width] = wall_char
    maze[starting_height][starting_width - 1] = wall_char
    maze[starting_height][starting_width + 1] = wall_char
    maze[starting_height + 1][starting_width] = wall_char

    while walls:
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        for neighbor in BIT_MAP:
            x = rand_wall[1] + neighbor[1]
            y = rand_wall[0] + neighbor[0]

            x_opposite = rand_wall[1] - neighbor[1]
            y_opposite = rand_wall[0] - neighbor[0]

            if neighbor[0] == 0 and (rand_wall[1] == 0 or rand_wall[1] == width - 1):
                continue
            elif neighbor[1] == 0 and (rand_wall[0] == 0 or rand_wall[0] == height - 1):
                continue

            if (maze[y][x] == unvisited_char
                    and maze[y_opposite][x_opposite] == cell_char):

                maze, s_cells = surrounding_cells(maze, rand_wall)

                if s_cells > 2:
                    continue

                maze[rand_wall[0]][rand_wall[1]] = cell_char

                if rand_wall[0] != 0:
                    if maze[rand_wall[0] - 1][rand_wall[1]] != cell_char:
                        maze[rand_wall[0] - 1][rand_wall[1]] = wall_char

                    if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                        walls.append([rand_wall[0] - 1, rand_wall[1]])

                if rand_wall[0] != height - 1:
                    if maze[rand_wall[0] + 1][rand_wall[1]] != cell_char:
                        maze[rand_wall[0] + 1][rand_wall[1]] = wall_char
                    if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                        walls.append([rand_wall[0] + 1, rand_wall[1]])

                if rand_wall[1] != 0:
                    if maze[rand_wall[0]][rand_wall[1] - 1] != cell_char:
                        maze[rand_wall[0]][rand_wall[1] - 1] = wall_char
                    if [rand_wall[0], rand_wall[1] - 1] not in walls:
                        walls.append([rand_wall[0], rand_wall[1] - 1])

                if rand_wall[1] != width - 1:
                    if maze[rand_wall[0]][rand_wall[1] + 1] != cell_char:
                        maze[rand_wall[0]][rand_wall[1] + 1] = wall_char
                    if [rand_wall[0], rand_wall[1] + 1] not in walls:
                        walls.append([rand_wall[0], rand_wall[1] + 1])

            for wall in walls:
                if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                    walls.remove(wall)

            continue

    walls = []

    for i in range(height):
        for j in range(width):
            if maze[i][j] == unvisited_char:
                maze[i][j] = wall_char

            if maze[i][j] == wall_char and i != 0 and j != 0 and j != height - 1 and i != width - 1:
                walls.append((j, i))

    walls_count = len(walls) // 10
    for i in range(walls_count):
        wall = random.choice(walls)

        maze[wall[1]][wall[0]] = cell_char

    maze[0][0] = 'e'
    maze[0][1] = '.'
    maze[-1][-1] = 's'

    if maze[-1][-2] != '.' and maze[-2][-1] != '.':
        if maze[-1][-3] == '.':
            maze[-1][-2] = '.'
        else:
            maze[-2][-1] = '.'

    return maze
