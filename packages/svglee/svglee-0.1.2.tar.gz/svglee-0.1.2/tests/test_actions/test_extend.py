from svglee import Arc, CBezier, Coordinate, Line, QBezier


def test_extend_line_with_line() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(2, 2)
    c3 = Coordinate(5, 4)

    group = Line(c1, c2).extend_line(c3)

    assert isinstance(group.elements[0], Line)
    assert isinstance(group.elements[1], Line)
    assert group.elements[0].coordinates() == [c1, c2]
    assert group.elements[1].coordinates() == [c2, c3]


def test_extend_line_with_qbezier() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(2, 2)
    c3 = Coordinate(5, 4)

    group = Line(c1, c2).extend_qbezier(c3)

    assert isinstance(group.elements[0], Line)
    assert isinstance(group.elements[1], QBezier)
    assert group.elements[0].coordinates() == [c1, c2]
    assert group.elements[1].coordinates() == [c2, c1.copy().rotate(180, c2), c3]


def test_extend_line_with_cbezier() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(2, 2)
    c3 = Coordinate(5, 4)
    c4 = Coordinate(8, 1)

    group = Line(c1, c2).extend_cbezier(c3, c4)

    assert isinstance(group.elements[0], Line)
    assert isinstance(group.elements[1], CBezier)
    assert group.elements[0].coordinates() == [c1, c2]
    assert group.elements[1].coordinates() == [c2, c1.copy().rotate(180, c2), c3, c4]


def test_extend_line_with_arc() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(2, 2)
    c3 = Coordinate(5, 4)

    group = Line(c1, c2).extend_arc(180, c3)

    assert isinstance(group.elements[0], Line)
    assert isinstance(group.elements[1], Arc)
    assert group.elements[0].coordinates() == [c1, c2]
    assert group.elements[1].coordinates() == [c2, c3, c2.copy().rotate(180, c3)]


def test_extend_qbezier_with_line() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(2, 2)
    c3 = Coordinate(5, 4)
    c4 = Coordinate(9, 9)

    group = QBezier(c1, c2, c3).extend_line(c4)

    assert isinstance(group.elements[0], QBezier)
    assert isinstance(group.elements[1], Line)
    assert group.elements[0].coordinates() == [c1, c2, c3]
    assert group.elements[1].coordinates() == [c3, c4]


def test_extend_qbezier_with_qbezier() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(2, 2)
    c3 = Coordinate(5, 4)
    c4 = Coordinate(9, 9)

    group = QBezier(c1, c2, c3).extend_qbezier(c4)

    assert isinstance(group.elements[0], QBezier)
    assert isinstance(group.elements[1], QBezier)
    assert group.elements[0].coordinates() == [c1, c2, c3]
    assert group.elements[1].coordinates() == [c3, c2.copy().rotate(180, c3), c4]


def test_extend_qbezier_with_cbezier() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(2, 2)
    c3 = Coordinate(5, 4)
    c4 = Coordinate(6, 6)
    c5 = Coordinate(9, 9)

    group = QBezier(c1, c2, c3).extend_cbezier(c4, c5)

    assert isinstance(group.elements[0], QBezier)
    assert isinstance(group.elements[1], CBezier)
    assert group.elements[0].coordinates() == [c1, c2, c3]
    assert group.elements[1].coordinates() == [c3, c2.copy().rotate(180, c3), c4, c5]


def test_extend_qbezier_with_arc() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(2, 2)
    c3 = Coordinate(5, 4)
    c4 = Coordinate(9, 9)

    group = QBezier(c1, c2, c3).extend_arc(120, c4)

    assert isinstance(group.elements[0], QBezier)
    assert isinstance(group.elements[1], Arc)
    assert group.elements[0].coordinates() == [c1, c2, c3]
    assert group.elements[1].coordinates() == [c3, c4, c3.copy().rotate(-120, c4)]
