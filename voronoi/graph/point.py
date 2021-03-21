import numpy as np

from voronoi.graph.vertex import Vertex
from voronoi.graph.coordinate import DecimalCoordinate


class Point(DecimalCoordinate):

    def __init__(self, x=None, y=None, metadata=None, name=None, first_edge=None):
        """
        A point in 2D space.
        :param x: (float) The x-coordinate
        :param y: (float) The y-coordinate
        :param metadata: (dict) Optional metadata stored in a dictionary
        :param name: (str) A one-letter string (assigned automatically by algorithm)
        :param first_edge: (HalfEdge) Pointer to the first edge (assigned automatically by the algorithm)
        """
        super().__init__(x, y)

        if metadata is None:
            metadata = {}

        self.metadata = metadata
        self.name = name
        self.first_edge = first_edge

    def __repr__(self):
        if self.name is not None:
            return f"P{self.name}"
        return f"Point({round(self.x, 3)}, {round(self.y, 3)})"

    def cell_size(self, digits=None):
        """
        Calculate cell size if the point is a site.
        :param digits: (int) number of digits to round to
        :return: (float) the area of the cell
        """
        x, y = self._get_xy()

        if digits is not None:
            return round(self._shoelace(x, y), digits)

        return self._shoelace(x, y)

    # Only returns answer when voronoi construction is complete, None otherwise
    def get_borders(self):
        edge = self.first_edge
        edges = [edge]
        while edge.next != self.first_edge:
            edge = edge.next
            edges.append(edge)
            if edge.next is None:
                return None
        return edges

    # Only returns answer when voronoi construction is complete, None otherwise
    def get_vertices(self):
        borders = self.get_borders()
        if borders is None:
            return None
        return [border.origin for border in borders if isinstance(border.origin, Vertex)]

    # Only returns answer when voronoi construction is complete, None otherwise
    def get_coordinates(self):
        borders = self.get_borders()
        if borders is None:
            return None
        coordinates = []
        for border in borders:

            # During construction, not all origins are vertices yet.
            origin = border.get_origin()
            if origin is None:
                return None

            coordinates.append(origin.as_floats())
        return coordinates

    def _get_xy(self):
        coordinates = self.get_coordinates()
        if coordinates is None:
            return [], []
        x = [coordinate.x for coordinate in coordinates]
        y = [coordinate.y for coordinate in coordinates]
        return x, y

    def __sub__(self, other):
        return Point(x=self.x-other.x, y=self.y-other.y)

    @staticmethod
    def _shoelace(x, y):
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
