from svglee import Collection, Coordinate, Line


def create_raster() -> Collection:
    elements = []
    for i in range(11):
        elements.append(Line(Coordinate(0, i), Coordinate(10, i)))
        elements.append(Line(Coordinate(i, 0), Coordinate(i, 10)))

    return Collection(*elements)
