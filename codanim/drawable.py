import pyglet
from pyglet import shapes

from codanim.element import Circle, Color, Element, Position


def add_to_batch(element: Element, batch: pyglet.graphics.Batch):
    # todo element could have cached list of subclass properties
    if isinstance(element, Circle):
        c = element
        return shapes.Circle(
            c.position.x, c.position.y, c.radius, color=c.color.as_tuple(), batch=batch
        )

    raise NotImplementedError


# def draw_scene(scene):
