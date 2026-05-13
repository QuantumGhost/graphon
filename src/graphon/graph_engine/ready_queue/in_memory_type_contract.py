from graphon.runtime.graph_runtime_state import ReadyQueueProtocol

from .in_memory import InMemoryReadyQueue


def _assert_in_memory_ready_queue_runtime_protocol(
    ready_queue: InMemoryReadyQueue,
) -> ReadyQueueProtocol:
    return ready_queue
