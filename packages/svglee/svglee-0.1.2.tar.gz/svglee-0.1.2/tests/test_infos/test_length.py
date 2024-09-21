from svglee import CBezier, Coordinate, Line, QBezier

C_1 = Coordinate(0, 0)
C_2 = Coordinate(0, 1)
C_3 = Coordinate(1, 0)
C_4 = Coordinate(1, 1)


def test_coordinate_length() -> None:
    element = Coordinate(1, 2)
    assert element.length() == 0.0


def test_line_length() -> None:
    element = Line(C_1, C_2)
    assert element.length()


def test_qbezier_lengths() -> None:
    element = QBezier(C_1, C_2, C_3)
    assert element.length()


def test_cbezier_lengths() -> None:
    element = CBezier(C_1, C_2, C_3, C_4)
    assert element.length()
