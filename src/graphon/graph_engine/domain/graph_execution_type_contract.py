from graphon.runtime.graph_runtime_state import GraphExecutionProtocol

from .graph_execution import GraphExecution


def _assert_graph_execution(
    execution: GraphExecution,
) -> GraphExecutionProtocol:
    return execution
