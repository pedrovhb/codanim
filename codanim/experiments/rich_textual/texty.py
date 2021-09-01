import asyncio

from rich.color import Color
from rich.style import Style
from rich.text import Text
from textual import events
from textual.app import App
from textual.reactive import Reactive
from textual.widgets import Footer, Placeholder, TreeControl, TreeClick, NodeID
from rich.tree import Tree
import networkx as nx


async def create_tree():
    g = nx.balanced_tree(2, 3)
    tree_ctrl = TreeControl(Text(str(0)), 0)
    tree = tree_ctrl.root

    visited = set()

    async def color(n, tree_node, it_num=1):
        visited.add(n)
        g.nodes[n]["subset"] = it_num

        new_node = await tree_node.add(Text(str(n)), n)

        for nei in g.neighbors(n):
            if nei in visited:
                continue
            await color(nei, new_node, it_num + 1)

    await color(0, tree)
    await tree.expand()
    for node in tree_ctrl.nodes.values():
        await node.expand()
    return tree_ctrl


class TreeApp(App):
    message_tree: TreeControl

    async def on_mount(self, event: events.Mount) -> None:
        self.message_tree = await create_tree()
        await self.view.dock(self.message_tree)
        asyncio.create_task(self.do_bfs())

    async def do_bfs(self):
        for node_number, node in self.message_tree.nodes.items():
            await asyncio.sleep(1)
            node.label.stylize(Style(color=Color.from_rgb(255, 0, 0)))
            self.message_tree.refresh()

    # async def message_tree_click(self, message: TreeClick) -> None:
    #     message.node.label.stylize(Style(color=Color.from_rgb(255, 255, 0)))
    #
    # async def message_tree_hover(self, message: TreeClick) -> None:
    #     message.node.label.stylize(Style(color=Color.from_rgb(255, 255, 0)))


TreeApp.run(log="textual.log")
