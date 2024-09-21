from enum import Enum
from typing import Generator

LINEARIZATION_PRECISION = 10000
FLOATINGPOINT_DECIMALS = 10


class PaperFormat(Enum):
    A0 = 1
    A1 = 2
    A2 = 3
    A3 = 4
    A4 = 5


PaperSize = {
    PaperFormat.A0: (84.1, 118.9, "cm"),
    PaperFormat.A1: (59.4, 84.1, "cm"),
    PaperFormat.A2: (42.0, 59.4, "cm"),
    PaperFormat.A3: (29.7, 42.0, "cm"),
    PaperFormat.A4: (21.0, 29.7, "cm"),
}


StyleDict = dict[str, str]


def linspace(start: int, stop: int, steps: int) -> Generator[float, None, None]:
    if steps == 1:
        yield stop
        return

    h = (stop - start) / (steps - 1)
    for i in range(steps):
        yield start + h * i
