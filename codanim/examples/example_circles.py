import pyglet

from codanim.element import Circle, Color, Position
from codanim.scene import StaticScene


class CirclesScene(StaticScene):

    # alternative - @pyglet_draw?
    def construct(self) -> list:
        circle = Circle(Position(300, 300), 30, Color(100, 100, 100))
        c2 = circle.but_with(position__x=320, color__r=255)
        # todo could just inspect locals to get list of elements
        #  instead of having to return a list? or both - use list
        #  if it's returned, otherwise use locals, or explicitly
        #  set list
        return [circle, c2]

    class Configs:
        enable_fps = True


if __name__ == "__main__":
    scene = CirclesScene()
    pyglet.clock.schedule_interval(scene.draw, 1 / 60)
    pyglet.app.run()
