from functools import cached_property
from typing import ClassVar, List, Protocol

import pyglet
from pyglet import shapes

from codanim.drawable import add_to_batch
from codanim.element import Element

# mixing concerns between scene and scene renderer for now, but temporary


class Renderer(Protocol):
    def draw(self, elements: List[Element]) -> None:
        ...


class PygletSceneRenderer(Renderer):
    def __init__(self, configs):
        self.elements = None
        # for eg pyglet.window.FPSDisplay(window=scene.renderer.window)
        # could be kwarg for fps?

        self.extra_drawables = []

        self.window = self.create_window()
        self.window.on_draw = self.on_draw

        if (enable_fps := getattr(configs, "enable_fps", None)) is not None:
            if enable_fps:  # not usefulf for a bool, but useful for others l8r
                fps_display = pyglet.window.FPSDisplay(window=self.window)
                self.extra_drawables.append(fps_display)

    def create_window(self):
        return pyglet.window.Window(960, 540)

    # @cached_property
    # def window(self) -> pyglet.window.Window:
    #     self._window = pyglet.window.Window(960, 540)
    #     self._window.on_draw = self.on_draw
    #     return self._window

    def draw(self, elements: List[Element]) -> None:
        self.elements = elements
        self.window.switch_to()
        # self.on_draw()

    def on_draw(self) -> None:
        self.window.clear()
        if not self.elements:
            print("No elements to draw.")
            return

        batch = pyglet.graphics.Batch()

        # have to keep references to batched objs
        # or pyglet will lose them by the time batch.draw()
        # is called
        refs = []
        for element in self.elements:
            refs.extend(element.add_to_batch(batch))

        batch.draw()
        for drawable in self.extra_drawables:
            drawable.draw()


class SceneBase:
    renderer_cls: ClassVar[type] = PygletSceneRenderer

    def construct(self):
        raise NotImplementedError

    @cached_property
    def renderer(self):
        return self.renderer_cls(self.Configs)

    class Configs:
        pass


class StaticScene(SceneBase):
    def construct(self) -> List[Element]:
        raise NotImplementedError

    def draw(self, dt):
        elements = self.construct()
        self.renderer.draw(elements)
