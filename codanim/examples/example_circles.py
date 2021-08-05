import pyglet
import jurigged

from codanim.element import Circle, Color, Position
from codanim.examples.run_example import CirclesScene
from codanim.scene import StaticScene

jurigged.watch(".")



if __name__ == "__main__":
    scene = CirclesScene()
    pyglet.clock.schedule_interval(scene.draw, 1 / 60)
    pyglet.app.run()
