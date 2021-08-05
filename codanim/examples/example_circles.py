from codanim.element import Circle, Position, Color
from codanim.scene import StaticScene


class CirclesScene(StaticScene):

    # alternative - @pyglet_draw?
    def construct(self) -> list:
        circle = Circle(Position(300, 300), 30, Color(120, 120, 255))
        c2 = circle.but_with(position__x=325, color__g=255)
        c3 = circle.but_with(color__r=255).with_offset(position__y=-25)

        c4 = c3.copy()
        c4.position.x = 200
        c4.color = c3.color.but_with(b=0)
        # todo could just inspect locals to get list of elements
        #  instead of having to return a list? or both - use list
        #  if it's returned, otherwise use locals, or explicitly
        #  set list
        return [circle, c2, c3, c4]

    class Configs:
        enable_fps = True
