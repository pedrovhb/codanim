import asyncio
import sys
from typing import List

from loguru import logger

from codanim.experiments.reactive.reactive import (
    Observer,
    reactive_observer,
    Observable,
    reactive_observable,
)


@reactive_observable
class Position(Observable):
    x: float
    y: float


@reactive_observable
class Circle(Observable):
    position: Position
    radius: float


@reactive_observer
class CircleDrawer(Observer):
    circle: Circle
    other_circle: Circle
    circle_list: List[Circle]


@logger.catch
async def main():
    p = Position(1, 10)
    c = Circle(p, 10)

    c2 = Circle(p, 20)

    clst = []
    batch_drawer = CircleDrawer(c, c2, clst)
    batch_drawer.circle = c
    batch_drawer.other_circle = c2
    # batch_drawer.circle_list.append(Circle(p, 15))


    p2 = Position(2, 20)
    c2.position = p2

    c.radius = 20
    p.x = 6
    p.y = 5
    print(p, p.x, p.y)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, backtrace=True, diagnose=True)
    logger.add(sys.stdout, level="TRACE")
    asyncio.run(main())
