from svglee import Collection, Coordinate, Line, QBezier
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


def test_fill_lines() -> None:
    document = Document(10, 10, "mm")
    raster = create_raster()
    c1 = Coordinate(3, 3)
    c2 = Coordinate(3, 6)
    c3 = Coordinate(6, 6)
    c4 = Coordinate(6, 3)
    group = (
        Line(c1, c2, {"fill": "green", "fill-opacity": "1"})
        .extend_line(c3)
        .extend_line(c4)
        .extend_line(c1)
    )

    document.add(raster, group)
    document.save("tests/test_svg/tmp/test_fill_line.svg", rotate=False)


def test_fill_qbezier() -> None:
    document = Document(10, 10, "mm")
    raster = create_raster()
    c1 = Coordinate(3, 3)
    c2 = Coordinate(3, 6)
    c3 = Coordinate(6, 6)
    c4 = Coordinate(6, 3)

    group = (
        QBezier(c1, c2, c3, {"fill": "green", "fill-opacity": "1"})
        .extend_qbezier(c4)
        .extend_qbezier(c1)
    )

    document.add(group)
    document.save("tests/test_svg/tmp/test_fill_qbezier.svg", rotate=False)
