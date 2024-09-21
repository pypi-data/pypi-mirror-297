from svglee import CBezier, Collection, Coordinate, Line, QBezier
from svglee.svg import Document

C_1 = Coordinate(0, 0)
C_2 = Coordinate(0, 10)
C_3 = Coordinate(10, 10)
C_4 = Coordinate(10, 0)


def raster() -> Collection:
    elements = []
    for i in range(11):
        elements.append(Line(Coordinate(0, i), Coordinate(10, i)))
        elements.append(Line(Coordinate(i, 0), Coordinate(i, 10)))

    return Collection(*elements)


def test_start_end_coordinaten() -> None:
    element = C_1

    # calculate
    start_coord = element.start
    end_coord = element.end

    # assert
    assert start_coord == element
    assert end_coord == element


def test_line_start_end() -> None:
    element = Line(C_1, C_2)
    element.update_styles({"stroke": "green"})

    # calculate
    start_coord = element.start
    end_coord = element.end
    reference = Collection(start_coord, end_coord)
    reference.update_styles({"stroke": "red"})

    # draw
    document = Document(10, 10, "cm")
    document.add(raster(), element, reference)
    document.save("tests/test_infos/tmp/test_start_end_line.svg")

    # assert
    assert start_coord == C_1
    assert end_coord == C_2


def test_qbezier_start_end() -> None:
    element = QBezier(C_1, C_2, C_3)
    element.update_styles({"stroke": "green"})

    # calculate
    start_coord = element.start
    end_coord = element.end
    reference = Collection(start_coord, end_coord)
    reference.update_styles({"stroke": "red"})

    # draw
    document = Document(10, 10, "cm")
    document.add(raster(), element, reference)
    document.save("tests/test_infos/tmp/test_start_end_qbezier.svg")

    # assert
    assert start_coord == C_1
    assert end_coord == C_3


def test_cbezier_start_end() -> None:
    element = CBezier(C_1, C_2, C_3, C_4)
    element.update_styles({"stroke": "green"})

    # calculate
    start_coord = element.start
    end_coord = element.end
    reference = Collection(start_coord, end_coord)
    reference.update_styles({"stroke": "red"})

    # draw
    document = Document(10, 10, "cm")
    document.add(raster(), element, reference)
    document.save("tests/test_infos/tmp/test_start_end_cbezier.svg")

    # assert
    assert start_coord == C_1
    assert end_coord == C_4


# def test_Element_not_connected() -> None:
#     C_1 = Coordinate(1, 5)
#     C_2 = Coordinate(5, 9)
#     element = Collection(C_1, C_2)

#     # calculate
#     with pytest.raises(Exception):
#         element.start

#     with pytest.raises(Exception):
#         element.end


def test_element_connected() -> None:
    l1 = Line(C_1, C_2)
    l2 = Line(C_2, C_3)
    element = Collection(l1, l2)
    element.update_styles({"stroke": "green"})

    # calculate
    start_coord = element.start
    end_coord = element.end
    reference = Collection(start_coord, end_coord)
    reference.update_styles({"stroke": "red"})

    # draw
    document = Document(10, 10, "cm")
    document.add(raster(), element, reference)
    document.save("tests/test_infos/tmp/test_start_end_element.svg")

    # assert
    assert start_coord == C_1
    assert end_coord == C_3
