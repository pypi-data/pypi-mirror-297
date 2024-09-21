import pytest

from svglee import CBezier, Collection, Coordinate, Line, QBezier
from svglee.svg import Document

from .. import create_raster


def test_coordinate_at_coordinate() -> None:
    element = Coordinate(1, 2)
    assert element.coordinate_at(0.0) == element
    assert element.coordinate_at(0.5) == element
    assert element.coordinate_at(1.0) == element


def test_line_coordinate_at() -> None:
    c1 = Coordinate(1, 2)
    c2 = Coordinate(3, 4)
    element = Line(c1, c2)

    assert element.coordinate_at(0.0) == c1
    assert element.coordinate_at(0.5) == Coordinate(
        0.5 * c1.x + 0.5 * c2.x, 0.5 * c1.y + 0.5 * c2.y
    )
    assert element.coordinate_at(1.0) == c2


def test_qbezier_coordinate_at() -> None:
    c1 = Coordinate(0, 0)
    c2 = Coordinate(0, 1)
    c3 = Coordinate(1, 1)
    element = QBezier(c1, c2, c3)

    assert element.coordinate_at(0.0) == c1
    assert element.coordinate_at(1.0) == c3


def test_coordinate_at_cbeziers() -> None:
    c1 = Coordinate(1, 1)
    c2 = Coordinate(7, 9)
    c3 = Coordinate(8, 3)
    c4 = Coordinate(9, 9)

    document = Document(10, 10, "mm")
    raster = create_raster()
    bezier = CBezier(c1, c2, c3, c4)
    x1 = bezier.coordinate_at(0.25, 10000)
    x2 = bezier.coordinate_at(0.5, 10000)
    x3 = bezier.coordinate_at(0.75, 10000)
    g_high = Collection(x1, x2, x3, styles={"stroke": "green"})
    x4 = bezier.coordinate_at(0.25, 10)
    x5 = bezier.coordinate_at(0.5, 10)
    x6 = bezier.coordinate_at(0.75, 10)
    g_low = Collection(x4, x5, x6, styles={"stroke": "red"})
    document.add(raster, bezier, c1, c2, c3, c4, g_high, g_low)
    document.save("tests/test_infos/tmp/test_coordinate_at_cbeziers.svg")


def test_element_coordinate_at() -> None:
    c1 = Coordinate(1, 2)
    c2 = Coordinate(3, 4)

    l1 = Line(c1, c2)
    element = Collection(c1, l1)
    assert element.coordinate_at(0.0) == c1
    assert element.coordinate_at(1.0) == c2


def test_element_coordinate_empty() -> None:
    element = Collection()
    with pytest.raises(Exception):
        element.coordinate_at(0.0)


# def test_element_coordinate_at_not_connected() -> None:
#     c1 = Coordinate(1, 2)
#     c2 = Coordinate(3, 4)
#     element = Collection(c1, c2)
#     with pytest.raises(Exception):
#         element.coordinate_at(0.5)


def test_element_coordinate_at_zero_length() -> None:
    c1 = Coordinate(1, 2)
    element = Collection(c1, c1)
    assert element.coordinate_at(0.0) == c1
