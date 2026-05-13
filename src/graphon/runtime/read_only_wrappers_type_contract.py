from .graph_runtime_state_protocol import ReadOnlyGraphRuntimeState
from .read_only_wrappers import ReadOnlyGraphRuntimeStateWrapper


def _assert_readonly_graph_runtime_state_wrapper(
    state: ReadOnlyGraphRuntimeStateWrapper,
) -> ReadOnlyGraphRuntimeState:
    return state
