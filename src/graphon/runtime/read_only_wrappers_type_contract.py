from .graph_runtime_state_protocol import (
    ReadOnlyGraphRuntimeState,
    ReadOnlyVariablePool,
)
from .read_only_wrappers import (
    ReadOnlyGraphRuntimeStateWrapper,
    ReadOnlyVariablePoolWrapper,
)


def _assert_readonly_variable_pool_wrapper(
    variable_pool: ReadOnlyVariablePoolWrapper,
) -> ReadOnlyVariablePool:
    return variable_pool


def _assert_readonly_graph_runtime_state_wrapper(
    state: ReadOnlyGraphRuntimeStateWrapper,
) -> ReadOnlyGraphRuntimeState:
    return state
