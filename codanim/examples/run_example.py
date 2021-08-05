import pyglet
import jurigged

from codanim.examples.example_circles import CirclesScene

jurigged.watch(".")


if __name__ == "__main__":
    scene = CirclesScene()
    pyglet.clock.schedule_interval(scene.draw, 1 / 60)
    pyglet.app.run()
