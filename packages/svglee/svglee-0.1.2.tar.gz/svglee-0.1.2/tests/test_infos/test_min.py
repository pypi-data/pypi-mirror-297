import math

from svglee import CBezier, Collection, Coordinate, Line, QBezier
from svglee.svg import Document

C_1 = Coordinate(1, 1)
C_2 = Coordinate(1, 11)
C_3 = Coordinate(11, 11)
C_4 = Coordinate(11, 1)


def raster() -> Collection:
    elements = []
    for i in range(11):
        elements.append(Line(Coordinate(1, 1 + i), Coordinate(11, 1 + i)))
        elements.append(Line(Coordinate(1 + i, 1), Coordinate(1 + i, 11)))

    return Collection(*elements)


def test_min_coordinaten() -> None:
    element = C_1

    # calculate
    min_coord = element.min_coordinate()
    max_coord = element.max_coordinate()

    # assert
    assert min_coord == element
    assert max_coord == element


def test_line_min_coordinate() -> None:
    element = Line(C_1, C_3)
    element.update_styles({"stroke": "green"})

    # calculate
    min_coord = element.min_coordinate()
    max_coord = element.max_coordinate()
    reference = Collection(min_coord, max_coord)
    reference.update_styles({"stroke": "red"})

    # draw
    document = Document(10, 10, "cm")
    document.add(raster(), element, reference)
    document.save("tests/test_infos/tmp/test_min_coordinate_line.svg")

    # assert
    assert min_coord == C_1
    assert max_coord == C_3


def test_qbezier_min_coordinate() -> None:
    element = QBezier(C_1, C_2, C_3)
    element.update_styles({"stroke": "green"})

    # calculate
    min_coord = element.min_coordinate()
    max_coord = element.max_coordinate()
    reference = Collection(min_coord, max_coord)
    reference.update_styles({"stroke": "red"})

    # draw
    document = Document(10, 10, "cm")
    document.add(raster(), element, reference)
    document.save("tests/test_infos/tmp/test_min_coordinate_qbezier.svg")

    # assert
    assert math.isclose(min_coord.x, C_1.x, rel_tol=1e-07)
    assert math.isclose(min_coord.y, C_1.y, rel_tol=1e-07)

    assert math.isclose(max_coord.x, C_3.x, rel_tol=1e-07)
    assert math.isclose(max_coord.y, C_3.y, rel_tol=1e-07)


def test_cbezier_min_coordinate() -> None:
    element = CBezier(C_1, C_2, C_3, C_4)
    element.update_styles({"stroke": "green"})

    # calculate
    min_coord = element.min_coordinate()
    max_coord = element.max_coordinate()
    reference = Collection(min_coord, max_coord)
    reference.update_styles({"stroke": "red"})

    # draw
    document = Document(10, 10, "cm")
    document.add(raster(), element, reference)
    document.save("tests/test_infos/tmp/test_min_coordinate_cbezier.svg")

    # assert
    assert math.isclose(min_coord.x, C_1.x, rel_tol=1e-07)
    assert math.isclose(min_coord.y, C_1.y, rel_tol=1e-07)

    assert math.isclose(max_coord.x, 11.0, rel_tol=1e-07)
    assert math.isclose(max_coord.y, 8.5, rel_tol=1e-07)


def test_element() -> None:
    l1 = Line(C_2, C_3)
    element = Collection(C_1, l1)
    element.update_styles({"stroke": "green"})

    # calculate
    min_coord = element.min_coordinate()
    max_coord = element.max_coordinate()
    reference = Collection(min_coord, max_coord)
    reference.update_styles({"stroke": "red"})

    # draw
    document = Document(10, 10, "cm")
    document.add(raster(), element, reference)
    document.save("tests/test_infos/tmp/test_min_coordinate_element.svg")

    # test  min coordinate
    assert min_coord == C_1
    assert max_coord == C_3
