from svglee import CBezier, Coordinate, Line, QBezier
from svglee.helper import linspace

C_1 = Coordinate(0, 0)
C_2 = Coordinate(0, 10)
C_3 = Coordinate(10, 10)
C_4 = Coordinate(10, 0)


def test_yield_one() -> None:
    points = list(linspace(0, 1, 10))
    assert points


def test_yield_many() -> None:
    points = []
    for point in linspace(0, 1, 2):
        points.append(point)

    assert points


def test_coordinate_linearize() -> None:
    element = C_1
    coordinates = [C_1]
    assert element.approximated_coordinates() == coordinates


def test_line_linearize() -> None:
    element = Line(C_1, C_2)
    assert element.approximated_coordinates() == element.elements


def test_qbezier_linearizes_k_3() -> None:
    element = QBezier(C_1, C_2, C_3)
    c_x = Coordinate(2.5, 7.5)
    coordinates = [C_1, c_x, C_3]
    assert element.approximated_coordinates(k=3) == coordinates


def test_cbezier_linearize() -> None:
    element = CBezier(C_1, C_2, C_3, C_4)
    coordinates = [Coordinate(0, 0), Coordinate(5.0, 7.5), Coordinate(10, 0)]
    assert element.approximated_coordinates(k=3) == coordinates
