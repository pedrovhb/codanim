import pyglet
import jurigged

from codanim.examples.example_circles import CirclesScene
from codanim.examples.example_values import ValuesScene



if __name__ == "__main__":
    jurigged.watch(".")
    scene = ValuesScene()
    pyglet.clock.schedule_interval(scene.draw, 1 / 60)
    pyglet.app.run()
