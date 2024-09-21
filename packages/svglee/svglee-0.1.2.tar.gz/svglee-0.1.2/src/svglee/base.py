from __future__ import annotations

import math
from collections import deque
from copy import deepcopy
from typing import Any, Self

from .helper import FLOATINGPOINT_DECIMALS, LINEARIZATION_PRECISION, linspace

StyleDict = dict[str, str]


class Coordinate:
    def __init__(self, x: float, y: float, styles: StyleDict | None = None) -> None:
        self.x = x
        self.y = y
        self.styles = styles or {}

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Coordinate):
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        return False

    def __str__(self) -> str:
        return f"Coordinate(x: {self.x:.2f}, y: {self.y:.2f})"

    def __repr__(self) -> str:
        return self.__str__()

    def translate(self, dx: float, dy: float) -> Coordinate:
        return Coordinate(self.x + dx, self.y + dy)

    def scale(self, dx: float, dy: float) -> Coordinate:
        return Coordinate(self.x * dx, self.y * dy)

    def rotate(self, rho: float, origin: Coordinate | None = None) -> Coordinate:
        origin = origin or Coordinate(0, 0)
        normalized = self.copy().translate(-origin.x, -origin.y)

        c = round(math.cos(math.radians(rho)), FLOATINGPOINT_DECIMALS)
        s = round(math.sin(math.radians(rho)), FLOATINGPOINT_DECIMALS)

        x = c * normalized.x - s * normalized.y + origin.x
        y = s * normalized.x + c * normalized.y + origin.y

        return Coordinate(x, y)

    def update_styles(self, styles: StyleDict) -> Self:
        self.styles.update(styles)
        return self

    def copy(self) -> Coordinate:
        return deepcopy(self)

    @property
    def start(self) -> Coordinate:
        return self.copy()

    @property
    def end(self) -> Coordinate:
        return self.copy()

    def approximated_coordinates(self, k=LINEARIZATION_PRECISION) -> list[Coordinate]:
        return [self.copy()]

    def approximated(self, k=LINEARIZATION_PRECISION) -> list[Line]:
        return [Line(self.copy(), self.copy())]

    def coordinate_at(self, t: float) -> Coordinate:
        return self.copy()

    def length(self) -> float:
        return 0.0

    def min_coordinate(self) -> Coordinate:
        return self.copy()

    def max_coordinate(self) -> Coordinate:
        return self.copy()

    def is_closed(self) -> bool:
        return False


class Path:
    def __init__(
        self,
        coordinate_1: Coordinate,
        coordinate_2: Coordinate,
        *coordinates: Coordinate,
        styles: StyleDict | None = None,
    ) -> None:
        self.elements = [
            e.copy() for e in [coordinate_1, coordinate_2] + list(coordinates)
        ]
        self.styles = styles or {}

    def __str__(self) -> str:
        internal = ", ".join([str(e) for e in self.elements])
        return f"{self.__class__.__name__}({internal})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.elements == other.elements

    def translate(self, dx: float, dy: float) -> Self:
        translated = self.copy()
        translated.elements = [e.translate(dx, dy) for e in self.elements]
        return translated

    def scale(self, dx: float, dy: float) -> Self:
        scaled = self.copy()
        scaled.elements = [e.scale(dx, dy) for e in self.elements]
        return scaled

    def rotate(self, rho: float, origin: Coordinate | None = None) -> Self:
        rotated = self.copy()
        rotated.elements = [e.rotate(rho, origin) for e in self.elements]
        return rotated

    def update_styles(self, styles: StyleDict) -> Self:
        self.styles.update(styles)
        return self

    def copy(self) -> Self:
        return deepcopy(self)

    @property
    def start(self) -> Coordinate:
        return self.copy().elements[0].start

    @property
    def end(self) -> Coordinate:
        return self.copy().elements[-1].end

    def approximated_coordinates(self, k=LINEARIZATION_PRECISION) -> list[Coordinate]:
        return NotImplemented

    def approximated(self, k=LINEARIZATION_PRECISION) -> list[Line]:
        c = self.approximated_coordinates(k)
        return [Line(c[i], c[i + 1]) for i in range(len(c) - 1)]

    def coordinate_at(self, t: float) -> Coordinate:
        return NotImplemented

    def length(self) -> float:
        return NotImplemented

    def min_coordinate(self) -> Coordinate:
        return NotImplemented

    def max_coordinate(self) -> Coordinate:
        return NotImplemented

    def coordinates(self) -> list[Coordinate]:
        return [item for item in self.copy().elements]

    def is_closed(self) -> bool:
        return self.start == self.end

    # Constructor
    def extend_line(
        self, end: Coordinate, styles: StyleDict | None = None
    ) -> Multipath:
        element = Line(self.end, end)
        return Multipath(self, element, styles=styles or self.styles)

    def extend_qbezier(
        self, end: Coordinate, styles: StyleDict | None = None
    ) -> Multipath:
        coordinates = self.coordinates()
        start = coordinates[-1]
        control = coordinates[-2].rotate(180, start)
        element = QBezier(start, control, end)
        return Multipath(self, element, styles=styles or self.styles)

    def extend_cbezier(
        self, control_2: Coordinate, end: Coordinate, styles: StyleDict | None = None
    ) -> Multipath:
        coordinates = self.coordinates()
        start = coordinates[-1]
        control_1 = coordinates[-2].rotate(180, start)
        element = CBezier(start, control_1, control_2, end)
        return Multipath(self, element, styles=styles or self.styles)

    def extend_arc(
        self, rho: float, center=Coordinate(0, 0), styles: StyleDict | None = None
    ) -> Multipath:
        coordinates = self.coordinates()
        start = coordinates[-1]
        element = Arc(start, rho, center)
        return Multipath(self, element, styles=styles or self.styles)


class Line(Path):
    def __init__(
        self, start: Coordinate, end: Coordinate, styles: StyleDict | None = None
    ) -> None:
        super().__init__(start, end, styles=styles)

    def approximated_coordinates(self, k=LINEARIZATION_PRECISION) -> list[Coordinate]:
        return self.coordinates()

    def coordinate_at(self, t: float) -> Coordinate:
        return Coordinate(
            (1 - t) * self.start.x + t * self.end.x,
            (1 - t) * self.start.y + t * self.end.y,
        )

    def length(self) -> float:
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return math.hypot(dx, dy)

    def min_coordinate(self) -> Coordinate:
        min_x = min(self.start.x, self.end.x)
        min_y = min(self.start.y, self.end.y)
        return Coordinate(min_x, min_y)

    def max_coordinate(self) -> Coordinate:
        max_x = max(self.start.x, self.end.x)
        max_y = max(self.start.y, self.end.y)
        return Coordinate(max_x, max_y)


class Bezier(Path):
    def __init__(
        self,
        *coordinate: Coordinate,
        styles: StyleDict | None = None,
    ):
        super().__init__(*coordinate, styles=styles)

    def de_casteljau(self, t: float, coefs: list[float]) -> float:
        beta = coefs.copy()  # values in this list are overridden
        n = len(beta)
        for j in range(1, n):
            for k in range(n - j):
                beta[k] = beta[k] * (1 - t) + beta[k + 1] * t
        return beta[0]

    def approximated_coordinates(self, k=LINEARIZATION_PRECISION) -> list[Coordinate]:
        x_coefs = [e.start.x for e in self.elements]
        y_coefs = [e.start.y for e in self.elements]
        return [
            Coordinate(self.de_casteljau(t, x_coefs), self.de_casteljau(t, y_coefs))
            for t in linspace(0, 1, k)
        ]

    def coordinate_at(self, t: float, k=LINEARIZATION_PRECISION) -> Coordinate:
        total = self.length()
        coords = self.approximated_coordinates(k)
        index = 0
        current = 0.0
        target: float = total * t
        while current < target and index < LINEARIZATION_PRECISION - 1:
            index += 1
            current += math.hypot(
                coords[index].x - coords[index - 1].x,
                coords[index].y - coords[index - 1].y,
            )

        return coords[index]

    def length(self, k=LINEARIZATION_PRECISION) -> float:
        coords = self.approximated_coordinates(k)
        return sum(
            math.hypot(coords[i + 1].x - coords[i].x, coords[i + 1].y - coords[i].y)
            for i in range(len(coords) - 1)
        )

    def min_coordinate(self, k=LINEARIZATION_PRECISION) -> Coordinate:
        coordinates = self.approximated_coordinates(k)
        min_x = min([coordinate.x for coordinate in coordinates])
        min_y = min([coordinate.y for coordinate in coordinates])
        return Coordinate(min_x, min_y)

    def max_coordinate(self, k=LINEARIZATION_PRECISION) -> Coordinate:
        coordinates = self.approximated_coordinates(k)
        max_x = max([coordinate.x for coordinate in coordinates])
        max_y = max([coordinate.y for coordinate in coordinates])
        return Coordinate(max_x, max_y)


class QBezier(Bezier):
    def __init__(
        self,
        start: Coordinate,
        control: Coordinate,
        end: Coordinate,
        styles: StyleDict | None = None,
    ):
        super().__init__(start, control, end, styles=styles)

    @property
    def control(self) -> Coordinate:
        return self.elements[1].start.copy()  # we know this is a coordinate


class CBezier(Bezier):
    def __init__(
        self,
        start: Coordinate,
        control_1: Coordinate,
        control_2: Coordinate,
        end: Coordinate,
        styles: StyleDict | None = None,
    ):
        super().__init__(start, control_1, control_2, end, styles=styles)

    @property
    def control_1(self) -> Coordinate:
        return self.elements[1].start.copy()

    @property
    def control_2(self) -> Coordinate:
        return self.elements[2].start.copy()


class Arc(Path):
    def __init__(
        self,
        start: Coordinate,
        rho: float,
        center: Coordinate | None = None,
        styles: StyleDict | None = None,
    ) -> None:
        self.rho = rho
        center = center or Coordinate(0, 0)
        end = start.rotate(rho, center)
        super().__init__(start, center, end, styles=styles)

    def sign(self, v: float) -> float:
        return -1.0 if v < 0 else 1.0

    def scale(self, dx: float, dy: float) -> Self:
        element = super().scale(dx, dy)
        element.rho *= self.sign(dx) * self.sign(dy)
        return element

    @property
    def centre(self) -> Coordinate:
        return self.elements[1].start.copy()

    def radius(self) -> float:
        dx = self.centre.x - self.start.x
        dy = self.centre.y - self.start.y
        return math.hypot(dx, dy)

    def approximated_coordinates(self, k=LINEARIZATION_PRECISION) -> list[Coordinate]:
        return self.coordinates()

    def coordinate_at(self, t: float) -> Coordinate:
        return self.start.rotate(self.rho * t, self.centre)

    def length(self) -> float:
        r = abs(math.hypot(self.start.x - self.centre.x, self.start.y - self.centre.y))
        return 2 * math.pi * r + self.rho / 180.0

    def min_coordinate(self, k=LINEARIZATION_PRECISION) -> Coordinate:
        coordinates = self.approximated_coordinates(k)
        min_x = min([coordinate.x for coordinate in coordinates])
        min_y = min([coordinate.y for coordinate in coordinates])
        return Coordinate(min_x, min_y)

    def max_coordinate(self, k=LINEARIZATION_PRECISION) -> Coordinate:
        coordinates = self.approximated_coordinates(k)
        max_x = max([coordinate.x for coordinate in coordinates])
        max_y = max([coordinate.y for coordinate in coordinates])
        return Coordinate(max_x, max_y)


class Multipath:
    def __init__(
        self,
        *elements: Path | Line | QBezier | CBezier | Arc,
        styles: StyleDict | None = None,
    ) -> None:
        self.elements = [e.copy() for e in list(elements)]
        self.styles = styles or {}

    def __str__(self) -> str:
        internal = ", ".join([str(e) for e in self.elements])
        return f"{self.__class__.__name__}({internal})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.elements == other.elements

    def translate(self, dx: float, dy: float) -> Self:
        elements = [e.translate(dx, dy) for e in self.elements]
        return self.__class__(*elements, styles=self.styles)

    def scale(self, dx: float, dy: float) -> Self:
        elements = [e.scale(dx, dy) for e in self.elements]
        return self.__class__(*elements, styles=self.styles)

    def rotate(self, rho: float, origin: Coordinate | None = None) -> Self:
        elements = [e.rotate(rho, origin) for e in self.elements]
        return self.__class__(*elements, styles=self.styles)

    def update_styles(self, styles: StyleDict) -> Self:
        self.styles.update(styles)
        return self

    def copy(self) -> Self:
        return deepcopy(self)

    @property
    def start(self) -> Coordinate:
        return self.elements[0].start.copy()

    @property
    def end(self) -> Coordinate:
        return self.elements[-1].end.copy()

    def approximated_coordinates(self, k=LINEARIZATION_PRECISION) -> list[Coordinate]:
        return [
            c
            for vec in [e.approximated_coordinates(k) for e in self.elements]
            for c in vec
        ]

    def approximated(self, k=LINEARIZATION_PRECISION) -> list[Line]:
        c = self.approximated_coordinates(k)
        return [Line(c[i], c[i + 1]) for i in range(len(c) - 1)]

    def coordinate_at(self, t: float) -> Coordinate:
        total = self.length()
        current = 0.0
        target = total * t

        for e in self.elements:
            this = e.length()
            if this < target - current:
                current += this
                continue

            if this != 0:
                approximated_t = (target - current) / this
            else:
                approximated_t = 0.0
            return e.coordinate_at(approximated_t)

        return self.end

    def length(self) -> float:
        return sum([e.length() for e in self.elements])

    def min_coordinate(self) -> Coordinate:
        coordinates = [e.min_coordinate() for e in self.elements]
        return Coordinate(
            min(coordinate.x for coordinate in coordinates),
            min(coordinate.y for coordinate in coordinates),
        )

    def max_coordinate(self) -> Coordinate:
        coordinates = [e.max_coordinate() for e in self.elements]
        return Coordinate(
            max(coordinate.x for coordinate in coordinates),
            max(coordinate.y for coordinate in coordinates),
        )

    def coordinates(self) -> list[Coordinate]:
        return [i for e in self.elements for i in e.coordinates()]

    def is_closed(self) -> bool:
        starts = deque(e.start for e in self.elements)
        ends = deque(e.end for e in self.elements)
        ends.rotate(1)
        return starts == ends

    # Constructor
    def extend_line(self, end: Coordinate) -> Self:
        element = self.elements[-1].extend_line(end).elements[-1]
        self.elements.append(element)
        return self

    def extend_qbezier(self, end: Coordinate) -> Self:
        element = self.elements[-1].extend_qbezier(end).elements[-1]
        self.elements.append(element)
        return self

    def extend_cbezier(self, control_2: Coordinate, end: Coordinate) -> Self:
        element = self.elements[-1].extend_cbezier(control_2, end).elements[-1]
        self.elements.append(element)
        return self

    def extend_arc(self, rho: int, centre: Coordinate) -> Self:
        element = self.elements[-1].extend_arc(rho, centre).elements[-1]
        self.elements.append(element)
        return self


class Collection(Multipath):
    def __init__(
        self,
        *elements: Coordinate | Line | QBezier | CBezier | Arc | Multipath | Collection,
        styles: StyleDict | None = None,
    ) -> None:
        self.elements = list(elements)
        self.styles = styles or {}

    def is_closed(self) -> bool:
        return False


Element = Coordinate | Path | Line | CBezier | QBezier | Arc | Multipath | Collection
