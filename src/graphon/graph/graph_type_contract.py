from graphon.runtime.graph_runtime_state import GraphProtocol

from .graph import Graph


def _assert_graph(graph: Graph) -> GraphProtocol:
    return graph
