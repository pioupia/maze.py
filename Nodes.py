from typing import List, Tuple

# Types
Coords = Tuple[int, int]


class Nodes:
    def __init__(self, coords: Coords, distance: int = 0):
        # X coords
        self.x: int = coords[0]

        # Y coords
        self.y: int = coords[1]

        # Distance of the exit point
        self.distance: int = distance

        # Neighbor list
        self.neighbor: List[Nodes] = []

    def set_distance(self, distance: int) -> None:
        """
        Allows you to define a new distance from the exit point

        :param distance: int
        :return: None
        """
        self.distance = distance

    def add_voisin(self, neighbor: 'Nodes') -> 'Nodes':
        """
        Allows you to add another (unique) neighbor if its not already in the
        neighbor list

        :param neighbor: 'Nodes'
        :return: 'Nodes'
        """
        if neighbor in self.neighbor:
            return self

        self.neighbor.append(neighbor)
        return self


def get_min_distance(points: List[Nodes]) -> Nodes | None:
    """
    Allows you to get the point with the shortest distance from the exit point.

    :param points: List[Nodes]
    :return: Nodes | None
    """
    if len(points) == 0:
        return None

    # The nearest point is the first neighbour
    near_point = points[0]
    for point in points:
        # If the current point is closer than our "closest" point)
        if point.distance < near_point.distance:
            # So we define it as "our nearest point".
            near_point = point

    return near_point
