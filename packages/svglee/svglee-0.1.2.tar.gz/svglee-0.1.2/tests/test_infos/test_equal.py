from svglee import CBezier, Collection, Coordinate, Line, QBezier

C_1 = Coordinate(0, 0)
C_2 = Coordinate(0, 1)
C_3 = Coordinate(1, 0)
C_4 = Coordinate(1, 1)


def test_coordinates_equal() -> None:
    assert C_1 == C_1
    assert not C_1 == C_2


def test_lines_equal() -> None:
    e_1 = Line(C_1, C_2)
    e_2 = Line(C_2, C_1)
    assert e_1 == e_1
    assert not e_1 == e_2


def test_qbeziers_equal() -> None:
    e_1 = QBezier(C_1, C_2, C_3)
    e_2 = QBezier(C_1, C_2, C_4)
    assert e_1 == e_1
    assert not e_1 == e_2


def test_cbeziers_equal() -> None:
    e_1 = CBezier(C_1, C_2, C_3, C_4)
    e_2 = CBezier(C_1, C_2, C_4, C_3)
    assert e_1 == e_1
    assert not e_1 == e_2


def test_element_equal() -> None:
    l_1 = Line(C_1, C_2)
    e_1 = Collection(C_1, l_1)
    e_2 = Collection(C_2, l_1)
    assert e_1 == e_1
    assert not e_1 == e_2
