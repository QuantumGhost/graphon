from .graph_runtime_state_protocol import ReadOnlyVariablePool
from .variable_pool import VariablePool


def _assert_readonly_variable_pool(pool: VariablePool) -> ReadOnlyVariablePool:
    # static assertion to ensure VariablePool implements the
    # ReadOnlyVariablePool.
    return pool
