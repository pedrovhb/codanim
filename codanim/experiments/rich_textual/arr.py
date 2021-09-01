from contextlib import contextmanager
from datetime import datetime
from typing import Any

from rich.align import Align
from rich.style import Style
from rich.text import Text

from textual.app import App
from textual.widget import Widget


class DataValue:
    def __init__(self, value: int, style: Style = None) -> None:
        self.value = value
        self.style = style

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        return Text(str(self.value))


# @contextmanager
class LL:
    def __init__(self, value: list[Any]) -> None:
        self.value = value
        self.index_styles = {}

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        return Text(str(self.value))


class ListStructure(Widget):
    def __init__(self, value: list[Any]) -> None:
        super().__init__()
        self.value = value

    async def on_mount(self, event):
        self.set_interval(1, callback=self.refresh)
        self.set_interval(1, callback=self.step_code)

    async def step_code(self):
        pass

    def render(self):
        # txt = Text(str(self.value))
        # txt = LL([1, 2, 3])
        txt = DataValue(3)
        return Align.center(DataValue(3), vertical="middle")


class ArrApp(App):
    async def on_mount(self, event):
        await self.view.dock(ListStructure([1, 2, 3]))


ArrApp.run()
