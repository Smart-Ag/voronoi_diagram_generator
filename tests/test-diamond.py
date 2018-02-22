from algorithm import Algorithm
from graph.bounding_box import BoundingBox
from graph.point import Point

points = [
    Point(5, 7.5),
    Point(2.5, 5),
    Point(7.5, 5),
    Point(6, 3),
]

v = Algorithm(BoundingBox(0, 10, 0, 10))
v.create_diagram(points=points, visualize_steps=False, verbose=True, visualize_result=True)

for point in v.points:
    print(point.cell_size(2), end=",")