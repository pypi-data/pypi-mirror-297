from svglee import CBezier, Coordinate, Line, QBezier

C_1 = Coordinate(0, 0)
C_2 = Coordinate(0, 1)
C_3 = Coordinate(1, 0)
C_4 = Coordinate(1, 1)


def test_coordinate_not_closed() -> None:
    coordinate = Coordinate(0, 0)
    assert not coordinate.is_closed()


def test_line_not_closed() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(1, 1)
    line = Line(c1, c2)
    assert not line.is_closed()


def test_qbezier_not_closed() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(1, 1)
    c3 = Coordinate(3, 1)
    qbezier = QBezier(c1, c2, c3)
    assert not qbezier.is_closed()


def test_qbezierclosed() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(1, 1)
    qbezier = QBezier(c1, c2, c1)
    assert qbezier.is_closed()


def test_cbezier_not_closed() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(1, 1)
    c3 = Coordinate(3, 1)
    c4 = Coordinate(5, 5)
    cbezier = CBezier(c1, c2, c3, c4)
    assert not cbezier.is_closed()


def test_cbezier_closed() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(1, 1)
    c3 = Coordinate(3, 1)
    cbezier = CBezier(c1, c2, c3, c1)
    assert cbezier.is_closed()


def test_multipath_not_closed() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(1, 1)
    c3 = Coordinate(3, 1)

    group = Line(c1, c2).extend_line(c3)
    assert not group.is_closed()


def test_multipath_closed() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(1, 1)
    c3 = Coordinate(3, 1)

    group = Line(c1, c2).extend_line(c3).extend_line(c1)
    assert group.is_closed()
