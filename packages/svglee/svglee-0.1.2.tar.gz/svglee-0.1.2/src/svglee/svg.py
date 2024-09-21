from xml.etree import ElementTree
from xml.etree.ElementTree import Element as SvgElement

from .base import (
    Arc,
    CBezier,
    Collection,
    Coordinate,
    Element,
    Line,
    Multipath,
    Path,
    QBezier,
)
from .helper import StyleDict

DEFAULT_STYLE: StyleDict = {"stroke-width": "0.01", "stroke": "black", "fill": "none"}


class BaseElement:
    def __init__(self, element: Element) -> None:
        self.element = element

    def extends(self) -> str:
        return " "

    def path(self) -> str:
        return f"M {self.element.start.x} {self.element.start.y} " + self.extends()

    def apply_style(self, svg: SvgElement) -> SvgElement:
        styles = DEFAULT_STYLE.copy()
        if self.element.styles:
            styles.update(self.element.styles)

        for k, v in styles.items():
            svg.set(k, v)
        return svg

    def svg(self) -> SvgElement:
        svg = SvgElement("empty")
        return svg


class CoordinateElement(BaseElement):
    def __init__(self, coordinate: Coordinate) -> None:
        self.element = coordinate

    def svg(self) -> SvgElement:
        svg = SvgElement(
            "circle", {"cx": str(self.element.x), "cy": str(self.element.y), "r": "0.1"}
        )
        svg = self.apply_style(svg)
        return svg


class LineElement(BaseElement):
    def __init__(self, line: Line) -> None:
        self.element = line

    def extends(self) -> str:
        return f"L {self.element.end.x},{self.element.end.y} "

    def svg(self) -> SvgElement:
        svg = SvgElement("path", {"d": self.path()})
        svg = self.apply_style(svg)
        return svg


class QBezierElement(BaseElement):
    def __init__(self, qbezier: QBezier) -> None:
        self.element = qbezier

    def extends(self) -> str:
        return f"Q {self.element.control.x},{self.element.control.y} {self.element.end.x},{self.element.end.y} "

    def svg(self) -> SvgElement:
        svg = SvgElement("path", {"d": self.path()})
        svg = self.apply_style(svg)
        return svg


class CBezierElement(BaseElement):
    def __init__(self, cbezier: CBezier) -> None:
        self.element = cbezier

    def extends(self) -> str:
        return f"C {self.element.control_1.x},{self.element.control_1.y} {self.element.control_2.x},{self.element.control_2.y}, {self.element.end.x},{self.element.end.y} "

    def svg(self) -> SvgElement:
        svg = SvgElement("path", {"d": self.path()})
        svg = self.apply_style(svg)
        return svg


class ArcElement(BaseElement):
    def __init__(self, arc: Arc) -> None:
        self.element = arc

    def extends(self) -> str:
        r = self.element.radius()
        lf = int(abs(self.element.rho) > 180)
        sf = int(self.element.rho > 0)
        return f"A {r} {r} 0 {lf} {sf} {self.element.end.x} {self.element.end.y} "

    def svg(self) -> SvgElement:
        svg = SvgElement("path", {"d": self.path()})
        svg = self.apply_style(svg)
        return svg


class MultipathElement(BaseElement):
    def __init__(self, multipath: Multipath) -> None:
        self.element = multipath

    def path(self) -> str:
        path = SvgElementFactory(self.element.elements[0]).path()
        for element in self.element.elements[1:]:
            path += SvgElementFactory(element).extends()
        return path

    def svg(self) -> SvgElement:
        svg = SvgElement("path", {"d": self.path()})
        svg = self.apply_style(svg)
        return svg


class CollectionElement(BaseElement):
    def __init__(self, collection: Collection) -> None:
        self.element = collection

    def svg(self) -> SvgElement:
        svg = SvgElement("g")

        for item in self.element.elements:
            svg_element = SvgElementFactory(item)
            svg_element.element.update_styles(self.element.styles)
            svg.append(svg_element.svg())

        svg = self.apply_style(svg)
        return svg


SvgElementType = (
    CoordinateElement
    | BaseElement
    | LineElement
    | CBezierElement
    | QBezierElement
    | ArcElement
    | MultipathElement
    | CollectionElement
)


class SvgElementFactory:
    def __new__(cls, element: Element) -> SvgElementType:
        match element:
            case Coordinate():
                return CoordinateElement(element)
            case Line():
                return LineElement(element)
            case CBezier():
                return CBezierElement(element)
            case QBezier():
                return QBezierElement(element)
            case Arc():
                return ArcElement(element)
            case Path():
                return BaseElement(element)
            case Collection():
                return CollectionElement(element)
            case Multipath():
                return MultipathElement(element)

        raise Exception()


class Document:
    def __init__(self, width: float, height: float, unit: str) -> None:
        self.width = width
        self.height = height
        self.unit = unit
        self.elements: list[Element] = []

    def add(self, *element: Element) -> None:
        # copy the elements so that eventual translations and scaling does not affect the original elements
        self.elements.extend([e.copy() for e in list(element)])

    def min_coordinate(self) -> Coordinate:
        coordinates = [e.min_coordinate() for e in self.elements]
        min_x = min(coordinate.x for coordinate in coordinates)
        min_y = min(coordinate.y for coordinate in coordinates)
        return Coordinate(min_x, min_y)

    def max_coordinate(self) -> Coordinate:
        coordinates = [e.max_coordinate() for e in self.elements]
        max_x = max(coordinate.x for coordinate in coordinates)
        max_y = max(coordinate.y for coordinate in coordinates)
        return Coordinate(max_x, max_y)

    def to_svg(self) -> SvgElement:
        document = SvgElement("svg")
        document.set("width", f"{self.width}{self.unit}")
        document.set("height", f"{self.height}{self.unit}")
        document.set("viewBox", f" 0 0 {self.width} {self.height}")
        document.set("xmlns", "http://www.w3.org/2000/svg")
        document.set("version", "1.1")

        for element in self.elements:
            svg_element = SvgElementFactory(element)
            svg = svg_element.svg()
            document.append(svg)
        return document

    def save(self, path: str, rotate=True, resize=False) -> None:
        if rotate:
            d = self.max_coordinate()
            self.elements = [e.scale(1, -1) for e in self.elements]
            self.elements = [e.translate(0, d.y) for e in self.elements]

        if resize:
            d = self.max_coordinate()
            self.width = d.x
            self.height = d.y

        data = ElementTree.tostringlist(self.to_svg())

        with open(path, "wb") as svg_file:
            svg_file.writelines(data)
