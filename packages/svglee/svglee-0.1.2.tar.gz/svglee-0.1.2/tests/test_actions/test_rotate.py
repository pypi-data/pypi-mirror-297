from svglee import Arc, CBezier, Coordinate, Line, Multipath, QBezier

RHO = -67

X1 = 1
Y1 = 2
X2 = 3
Y2 = 4
X3 = 6
Y3 = 5
X4 = 7
Y4 = 7


def test_rotate_coordinate() -> None:
    """
    000|0A0
    000|000
    ---|---
    000|00B
    000|000
    """
    initial = Coordinate(X1, Y1)
    scaled = initial.rotate(-90)

    assert scaled.x == 2
    assert scaled.y == -1


def test_rotate_line() -> None:
    initial = Line(Coordinate(X1, Y1), Coordinate(X2, Y2))
    scaled = initial.rotate(RHO)

    assert scaled.start == initial.start.rotate(RHO)
    assert scaled.end == initial.end.rotate(RHO)


def test_rotate_qbezier() -> None:
    initial = QBezier(Coordinate(X1, Y1), Coordinate(X2, Y2), Coordinate(X3, Y3))
    scaled = initial.rotate(RHO)

    assert scaled.start == initial.start.rotate(RHO)
    assert scaled.control == initial.control.rotate(RHO)
    assert scaled.end == initial.end.rotate(RHO)


def test_rotate_cbezier() -> None:
    initial = CBezier(
        Coordinate(X1, Y1), Coordinate(X2, Y2), Coordinate(X3, Y3), Coordinate(X4, Y4)
    )
    scaled = initial.rotate(RHO)

    assert scaled.start == initial.start.rotate(RHO)
    assert scaled.control_1 == initial.control_1.rotate(RHO)
    assert scaled.control_2 == initial.control_2.rotate(RHO)
    assert scaled.end == initial.end.rotate(RHO)


def test_rotate_arc() -> None:
    initial = Arc(Coordinate(X1, Y1), 180)
    scaled = initial.rotate(RHO)

    assert scaled.start == initial.start.rotate(RHO)
    assert scaled.centre == initial.centre.rotate(RHO)
    assert scaled.end == initial.end.rotate(RHO)


def test_rotate_multipath() -> None:
    l1 = Line(Coordinate(X1, Y1), Coordinate(X2, Y2))
    l2 = Line(Coordinate(X2, Y2), Coordinate(X3, Y3))

    initial = Multipath(l1, l2)
    scaled = initial.rotate(RHO)

    assert scaled.elements[0] == initial.elements[0].rotate(RHO)
    assert scaled.elements[1] == initial.elements[1].rotate(RHO)
