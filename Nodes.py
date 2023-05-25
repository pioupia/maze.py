from typing import List, Tuple

# Types
Coords = Tuple[int, int]


class Nodes:
    def __init__(self, coords: Coords, distance: int = 0):
        # Coordonnée x
        self.x: int = coords[0]

        # Coordonnée y
        self.y: int = coords[1]

        # Distance par rapport au point de sortie
        self.distance: int = distance

        # Liste des voisins
        self.voisins: List[Nodes] = []

    def set_distance(self, distance: int) -> None:
        """
        Permet de définir une nouvelle distance par rapport au point de sortie

        :param distance: int
        :return: None
        """
        self.distance = distance

    def add_voisin(self, voisin: 'Nodes') -> 'Nodes':
        """
        Permet d'ajouter un voisin (unique) s'il n'est pas déjà dans la liste
        des voisins.

        :param voisin: 'Nodes'
        :return: 'Nodes'
        """
        # Si le voisin à ajouter existe déjà, on ne fait rien
        if voisin in self.voisins:
            return self

        # Sinon on l'ajoute
        self.voisins.append(voisin)
        return self


def get_min_distance(points: List[Nodes]) -> Nodes | None:
    """
    Permet de récupérer le point ayant la plus faible distance
    du point de sortie.

    :param points: List[Nodes]
    :return: Nodes | None
    """
    # Aucun voisin (normalement le cas n'existe pas).
    if len(points) == 0:
        return None

    # Le point le plus proche est le premier voisin
    near_point = points[0]
    for point in points:
        # Si le point actuel est plus proche que notre point "le plus proche")
        if point.distance < near_point.distance:
            # Alors on le définit en tant que "notre point le plus proche"
            near_point = point

    return near_point
