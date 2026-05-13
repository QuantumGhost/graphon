from graphon.runtime.graph_runtime_state import NodeExecutionProtocol

from .node_execution import NodeExecution


def _assert_node_execution(
    execution: NodeExecution,
) -> NodeExecutionProtocol:
    return execution
