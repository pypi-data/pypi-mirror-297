from svglee import Arc, CBezier, Coordinate, Line, Multipath, QBezier

DX = 1
DY = 1.5

X1 = 1
Y1 = 2
X2 = 3
Y2 = 4
X3 = 6
Y3 = 5
X4 = 7
Y4 = 7


def test_scale_coordinate() -> None:
    initial = Coordinate(X1, Y1)
    scaled = initial.scale(DX, DY)

    assert scaled.x == initial.x * DX
    assert scaled.y == initial.y * DY


def test_scale_line() -> None:
    initial = Line(Coordinate(X1, Y1), Coordinate(X2, Y2))
    scaled = initial.scale(DX, DY)

    assert scaled.start == initial.start.scale(DX, DY)
    assert scaled.end == initial.end.scale(DX, DY)


def test_scale_qbezier() -> None:
    initial = QBezier(Coordinate(X1, Y1), Coordinate(X2, Y2), Coordinate(X3, Y3))
    scaled = initial.scale(DX, DY)

    assert scaled.start == initial.start.scale(DX, DY)
    assert scaled.control == initial.control.scale(DX, DY)
    assert scaled.end == initial.end.scale(DX, DY)


def test_scale_cbezier() -> None:
    initial = CBezier(
        Coordinate(X1, Y1), Coordinate(X2, Y2), Coordinate(X3, Y3), Coordinate(X4, Y4)
    )
    scaled = initial.scale(DX, DY)

    assert scaled.start == initial.start.scale(DX, DY)
    assert scaled.control_1 == initial.control_1.scale(DX, DY)
    assert scaled.control_2 == initial.control_2.scale(DX, DY)
    assert scaled.end == initial.end.scale(DX, DY)


def test_scale_arc() -> None:
    initial = Arc(Coordinate(X1, Y1), 180)
    scaled = initial.scale(DX, DY)

    assert scaled.start == initial.start.scale(DX, DY)
    assert scaled.centre == initial.centre.scale(DX, DY)
    assert scaled.end == initial.end.scale(DX, DY)


def test_scale_multipath() -> None:
    l1 = Line(Coordinate(X1, Y1), Coordinate(X2, Y2))
    l2 = Line(Coordinate(X2, Y2), Coordinate(X3, Y3))

    initial = Multipath(l1, l2)
    scaled = initial.scale(DX, DY)

    assert scaled.elements[0] == initial.elements[0].scale(DX, DY)
    assert scaled.elements[1] == initial.elements[1].scale(DX, DY)
