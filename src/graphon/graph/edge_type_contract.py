from graphon.runtime.graph_runtime_state import EdgeProtocol

from .edge import Edge


def _assert_edge(edge: Edge) -> EdgeProtocol:
    return edge
