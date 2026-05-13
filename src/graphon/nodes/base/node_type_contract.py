from typing import Any

from graphon.runtime.graph_runtime_state import NodeProtocol

from .node import Node


def _assert_node(node: Node[Any]) -> NodeProtocol:
    return node
