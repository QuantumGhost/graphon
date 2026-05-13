from graphon.nodes.runtime import ToolNodeRuntimeProtocol

from .tool_runtime import SlimToolNodeRuntime


def _assert_slim_tool_node_runtime(
    runtime: SlimToolNodeRuntime,
) -> ToolNodeRuntimeProtocol:
    return runtime
