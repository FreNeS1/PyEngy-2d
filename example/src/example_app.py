"""Contains the example app."""

from example.src.node import PingNode
from pyengy.app import App
from pyengy.node import Node, Node2D
from pyengy.node.graphics import Node2DSprite


def build_scene():
    """
    Builds the scene of the example app.

    :return: The example scene.
    """
    return Node("ROOT", children=[
        PingNode("PING_NODE_1s", 1000),
        PingNode("PING_NODE_2s", 2000),
        Node2D("BOX_STACK", position=(300, 200), rotation=0, scale=(2, 2), children=[
            Node2DSprite("BOX_BOTTOM_LEFT", "box.png", position=(0, 55), rotation=0, scale=(1, 1)),
            Node2DSprite("BOX_BOTTOM_RIGHT", "box.png", position=(110, 55), rotation=90, scale=(1, 1)),
            Node2DSprite("BOX_TOP", "box.png", position=(35, 12), rotation=0, scale=(1, 1), texture_offset=(6, 6),
                         texture_size=(43, 43)),
        ])
    ])


if __name__ == '__main__':
    app = App("test_app", scene=build_scene(), resource_path="resources", window_size=(640, 480), fullscreen=False)
    app.start()
    app.wait()
