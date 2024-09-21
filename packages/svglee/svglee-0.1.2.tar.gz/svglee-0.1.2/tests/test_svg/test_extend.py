from svglee import CBezier, Collection, Coordinate, Line, QBezier
from svglee.base import Multipath
from svglee.svg import Document


def create_raster() -> Collection:
    elements = []
    for i in range(11):
        elements.append(Line(Coordinate(0, i), Coordinate(10, i)))
        elements.append(Line(Coordinate(i, 0), Coordinate(i, 10)))

    return Collection(*elements)


def test_document() -> None:
    document = Document(10, 10, "cm")
    print(document)


def test_coordinate() -> None:
    document = Document(10, 10, "mm")
    raster = create_raster()
    coordinate = Coordinate(5, 5, {"stroke": "green"})
    document.add(raster, coordinate)
    document.save("tests/test_svg/tmp/test_coordinate.svg")


def test_line_extend_qbezier() -> None:
    document = Document(10, 10, "mm")
    raster = create_raster()
    c1 = Coordinate(1, 1)
    c2 = Coordinate(6, 6)
    c3 = Coordinate(9, 3)
    line = Line(c1, c2, {"stroke": "green"})
    bezier = QBezier(c2, c1.copy().rotate(180, c2), c3, {"stroke": "red"})

    group: Multipath = line.extend_qbezier(c3)
    document.add(raster, line, bezier, group)
    document.save("tests/test_svg/tmp/test_extend_line_qbezier.svg")


def test_qbezier() -> None:
    document = Document(10, 10, "mm")
    raster = create_raster()
    c1 = Coordinate(1, 1)
    c2 = Coordinate(3, 6)
    c3 = Coordinate(6, 3)
    c4 = Coordinate(9, 9)
    qbezier = QBezier(c1, c2, c3, {"stroke": "green"})
    cbezier = CBezier(c1, c2, c3, c4, {"stroke": "red"})

    document.add(raster, qbezier, cbezier)
    document.save("tests/test_svg/tmp/test_qbezier.svg")
