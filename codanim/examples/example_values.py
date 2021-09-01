from codanim.element import Circle, Position, Color, CircleWithValue
from codanim.scene import StaticScene


class ValuesScene(StaticScene):

    # alternative - @pyglet_draw?
    def construct(self) -> list:
        cv = CircleWithValue(
            position=Position(500, 500),
            value=":]",
            circle=Circle(
                position=Position.from_parent(),
                radius=20,
                color=Color(100, 120, 30),
            ),
        )

        # [2021-08-09 10:24 AM] todo - parameters shouldn't be all customizable
        # at declaration time - won't make much sense to be setting circle props
        # way down in high level components.

        # [2021-08-06 08:08 PM] todo - possibility -
        # [2021-08-06 08:08 PM] cv.but_with(value=1, position__x=Offset(20))
        tree_repr = [
            cv.but_with(value=1),
            cv.but_with(value=1),
            cv.but_with(value=1),
        ]

        return [cv, *tree_repr]

    class Configs:
        enable_fps = True
