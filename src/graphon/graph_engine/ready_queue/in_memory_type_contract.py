from graphon.runtime.graph_runtime_state import ReadyQueueProtocol

from .in_memory import InMemoryReadyQueue
from .protocol import ReadyQueue


def _assert_in_memory_ready_queue(
    ready_queue: InMemoryReadyQueue,
) -> ReadyQueue:
    return ready_queue


def _assert_in_memory_ready_queue_runtime_protocol(
    ready_queue: InMemoryReadyQueue,
) -> ReadyQueueProtocol:
    return ready_queue
