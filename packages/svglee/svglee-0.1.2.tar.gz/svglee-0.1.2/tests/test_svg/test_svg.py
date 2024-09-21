from svglee import Arc, CBezier, Collection, Coordinate, Line, QBezier
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
    document = Document(10, 10, "cm")
    raster = create_raster()
    coordinate = Coordinate(5, 5, {"stroke": "green"})
    document.add(raster, coordinate)
    document.save("tests/test_svg/tmp/test_coordinate.svg")


def test_line() -> None:
    document = Document(10, 10, "cm")
    raster = create_raster()
    c1 = Coordinate(1, 1)
    c2 = Coordinate(9, 7)
    line = Line(c1, c2, {"stroke": "green"})
    document.add(raster, line)
    document.save("tests/test_svg/tmp/test_line.svg")


def test_qbezier() -> None:
    document = Document(10, 10, "cm")
    raster = create_raster()
    c1 = Coordinate(1, 1)
    c2 = Coordinate(3, 6)
    c3 = Coordinate(6, 3)
    c4 = Coordinate(9, 9)
    qbezier = QBezier(c1, c2, c3, {"stroke": "green"})

    document.add(raster, qbezier)
    document.save("tests/test_svg/tmp/test_qbezier.svg")


def test_cbezier() -> None:
    document = Document(10, 10, "cm")
    raster = create_raster()
    c1 = Coordinate(1, 1)
    c2 = Coordinate(3, 6)
    c3 = Coordinate(6, 3)
    c4 = Coordinate(9, 9)
    cbezier = CBezier(c1, c2, c3, c4, {"stroke": "red"})

    document.add(raster, cbezier)
    document.save("tests/test_svg/tmp/test_cbezier.svg")


def test_arc() -> None:
    document = Document(10, 10, "cm")
    raster = create_raster()
    c1 = Coordinate(5, 5)
    c2 = Coordinate(3, 3)
    arc1 = Arc(c1, 60, c2, styles={"stroke": "green"})
    arc2 = Arc(c1, 60, c2).scale(-1, 1).translate(10, 0)
    arc3 = Arc(c1, 60, c2).scale(1, -1).translate(0, 10)
    arc4 = Arc(c1, 60, c2).scale(-1, -1).translate(10, 10)
    g1 = Collection(arc1, arc1.start, arc1.centre, arc1.end, styles={"stroke": "green"})
    g2 = Collection(arc2, arc2.start, arc2.centre, arc2.end, styles={"stroke": "red"})
    g3 = Collection(arc3, arc3.start, arc3.centre, arc3.end, styles={"stroke": "blue"})
    g4 = Collection(arc4, arc4.start, arc4.centre, arc4.end, styles={"stroke": "black"})
    document.add(raster, g1, g2, g3, g4)
    document.save("tests/test_svg/tmp/test_arc.svg", rotate=True)


def test_arc_path() -> None:
    document = Document(10, 10, "cm")
    raster = create_raster()
    c0 = Coordinate(2, 3)
    c1 = Coordinate(5, 5)
    c2 = Coordinate(3, 3)
    line1 = Line(c0, c1)
    arc = line1.extend_arc(60, c2)
    line2 = arc.extend_line(c0)
    g = Collection(line1, arc, line2, styles={"fill": "green"})
    document.add(raster, g)

    document.save("tests/test_svg/tmp/test_arc_path.svg", rotate=True)
