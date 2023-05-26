from typing import Dict
import pygame
from pygame.locals import *
from Nodes import *
from generate_maze import generate_maze

# We create a BIT_MAP variable to know were the neighbor coords are.
BIT_MAP = [[1, 0], [-1, 0], [0, 1], [0, -1]]

# Types
GameMap = List[List[str]]
Path = List[Nodes]


class Waze:
    """
    Search a path in the waze.
    """

    def __init__(self, waze: GameMap):
        """ Create a waze from a 2D char list """

        # We're defining the window and the cell size to None
        self.window = None
        self.cell_size = None

        self.height = len(waze)
        self.width = len(waze[0])

        # We're creating an empty dictionary
        self.adjacency_list: Dict[Coords, Nodes] = {}

        # Our entry and exit coords (tuple (x,y)).
        self.entree: Coords | None = None
        self.sortie: Coords | None = None

        # Check the entry and exit coords in the same times
        self.get_entry_exit(waze)

        # We're generating a adjacency list from the waze datas
        self.create_adjacency_list(waze)

        # Drawing our beautiful waze
        self.draw(waze)

    def get_entry_exit(self, waze: GameMap):
        """
        Allows you to affect coords to the entry and the exit of the waze, to the entry and exit attribute
        """
        for y in range(self.height):
            for x in range(self.width):
                if waze[y][x] == "e":  # If its the entry
                    self.entree = (x, y)  # Set the entry coords
                    self.adjacency_list[self.entree] = Nodes(self.entree)  # And link a nodes to it.
                elif waze[y][x] == "s":  # Same process
                    self.sortie = (x, y)
                    self.adjacency_list[self.sortie] = Nodes(self.sortie, -1)

                # No more things to see
                if self.sortie and self.entree:
                    return

    def create_adjacency_list(self, maze: GameMap):
        """
        Create the adjacency list of the graph which represent the waze
        """
        for y in range(self.height):
            for x in range(self.width):
                if maze[y][x] != "#":  # Check if it's not a wall
                    key = (x, y)  # Defining it a key

                    if key not in self.adjacency_list:  # If the key is not in our adjacency list
                        self.adjacency_list[key] = Nodes(key)  # Create it!

                    # Define our nodes, more efficiency for getting the values.
                    node = self.adjacency_list[key]

                    # Getting all neighbors with our BIT MAP
                    for neighbor in BIT_MAP:
                        # Calculate its coords
                        neighbor_coord = (x + neighbor[0], y + neighbor[1])
                        (neighbor_x, neighbor_y) = neighbor_coord

                        # Verify the coords does not goes out of the waze
                        if neighbor_y < 0 or neighbor_y >= self.height or neighbor_x < 0 or neighbor_x >= self.width:
                            continue

                        if neighbor_coord not in self.adjacency_list:
                            self.adjacency_list[neighbor_coord] = Nodes(neighbor_coord)

                        if maze[neighbor_y][neighbor_x] != '#':
                            node.add_voisin(self.adjacency_list[neighbor_coord])

            self.set_distance_from_end(self.adjacency_list[self.sortie], self.adjacency_list[self.entree])

    def set_distance_from_end(self, point: Nodes, start_point: Nodes, distance=1) -> None:
        """
        Allows you to determine all the distance from the ending point for each node.

        :param point: Nodes - Ending nodes.
        :param start_point: Nodes - Starting nodes
        :param distance: int (Distance from the ending nodes)
        :return: None
        """
        # Get all the neighbor of the actual point
        for voisin in point.neighbor:

            # If the algorithm found the starting point before the other points
            # and the starting point distance is nearest than the actual distance
            # just stop the recursion
            if start_point.distance != 0 and start_point.distance <= distance:
                return

            # If this neighbor has the default distance value or its distance
            # is higher than the actual, we've a shortest path.
            if voisin.distance == 0 or voisin.distance > distance:
                # So we define a new distance
                voisin.set_distance(distance)
                # And we ask to do the same thing for all the neighbor of this node.
                self.set_distance_from_end(voisin, start_point, distance + 1)

    def draw(self, waze: GameMap):
        """
        Main method which manages all displays.
        """
        pygame.init()

        monitor_size = pygame.display.Info()

        self.cell_size = (monitor_size.current_w / 1.5) // self.width

        self.window = pygame.display.set_mode((self.cell_size * self.width, self.cell_size * self.height))

        self.draw_maze(waze)

        path = self.find_nearest_path()

        self.draw_path(path)

        can_continue = 1
        while can_continue:
            for event in pygame.event.get():
                if event.type == QUIT:
                    can_continue = 0

        pygame.quit()

    def draw_maze(self, waze):
        """
        Draw the waze.

        Black cells represent walls.
        """
        carre = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)

        for y in range(self.height):
            for x in range(self.width):
                color = (0, 0, 0, 255)

                if waze[y][x] == ".":
                    color = (255, 255, 255, 255)
                elif waze[y][x] == "s":
                    color = (0, 255, 0, 255)
                elif waze[y][x] == "e":
                    color = (255, 0, 0, 255)

                carre.fill(color)
                self.window.blit(carre, (x * self.cell_size, y * self.cell_size))

        pygame.display.flip()

    def draw_path(self, path: Path):
        """
        Draw the path in the maze
        """
        color = (255, 0, 0, 255)
        path_size = len(path) - 1

        for i in range(path_size):
            pygame.draw.line(
                self.window,
                color,
                (
                    path[i].x * self.cell_size + int(self.cell_size / 2),
                    path[i].y * self.cell_size + int(self.cell_size / 2)
                ),
                (
                    path[i + 1].x * self.cell_size + int(self.cell_size / 2),
                    path[i + 1].y * self.cell_size + int(self.cell_size / 2)
                ),
                5
            )

        pygame.display.flip()

    def find_nearest_path(self) -> Path:
        """
        Find the nearest path
        """
        # We're getting the entry node
        start = self.adjacency_list[self.entree]

        # Exit nodes
        end = self.adjacency_list[self.sortie]

        # Initialize the chain
        chain = [start]

        # While it not complete
        while start != end:
            # We're taking the nearest neighbor of this point which has the lowest distance from the exit.
            start = get_min_distance(start.neighbor)

            # If he found nothing. No path.
            if start is None:
                return []

            # Else, we add our point to the chain.
            chain.append(start)

        return chain


Waze(generate_maze(30, 20))
