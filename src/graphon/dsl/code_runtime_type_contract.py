from graphon.nodes.code.code_node import CodeExecutorProtocol

from .code_runtime import SandboxCodeExecutor


def _assert_sandbox_code_executor(
    executor: SandboxCodeExecutor,
) -> CodeExecutorProtocol:
    return executor
