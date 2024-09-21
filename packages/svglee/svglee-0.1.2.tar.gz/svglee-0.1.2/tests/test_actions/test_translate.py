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


def test_translate_coordinate() -> None:
    initial = Coordinate(X1, Y1)
    scaled = initial.translate(DX, DY)

    assert scaled.x == initial.x + DX
    assert scaled.y == initial.y + DY


def test_translate_line() -> None:
    initial = Line(Coordinate(X1, Y1), Coordinate(X2, Y2))
    scaled = initial.translate(DX, DY)

    assert scaled.start == initial.start.translate(DX, DY)
    assert scaled.end == initial.end.translate(DX, DY)


def test_translate_qbezier() -> None:
    initial = QBezier(Coordinate(X1, Y1), Coordinate(X2, Y2), Coordinate(X3, Y3))
    scaled = initial.translate(DX, DY)

    assert scaled.start == initial.start.translate(DX, DY)
    assert scaled.control == initial.control.translate(DX, DY)
    assert scaled.end == initial.end.translate(DX, DY)


def test_translate_cbezier() -> None:
    initial = CBezier(
        Coordinate(X1, Y1), Coordinate(X2, Y2), Coordinate(X3, Y3), Coordinate(X4, Y4)
    )
    scaled = initial.translate(DX, DY)

    assert scaled.start == initial.start.translate(DX, DY)
    assert scaled.control_1 == initial.control_1.translate(DX, DY)
    assert scaled.control_2 == initial.control_2.translate(DX, DY)
    assert scaled.end == initial.end.translate(DX, DY)


def test_translate_arc() -> None:
    initial = Arc(Coordinate(X1, Y1), 180)
    scaled = initial.translate(DX, DY)

    assert scaled.start == initial.start.translate(DX, DY)
    assert scaled.centre == initial.centre.translate(DX, DY)
    assert scaled.end == initial.end.translate(DX, DY)


def test_translate_multipath() -> None:
    l1 = Line(Coordinate(X1, Y1), Coordinate(X2, Y2))
    l2 = Line(Coordinate(X2, Y2), Coordinate(X3, Y3))

    initial = Multipath(l1, l2)
    scaled = initial.translate(DX, DY)

    assert scaled.elements[0] == initial.elements[0].translate(DX, DY)
    assert scaled.elements[1] == initial.elements[1].translate(DX, DY)
