from graphon.runtime.graph_runtime_state import ResponseStreamCoordinatorProtocol

from .coordinator import ResponseStreamCoordinator


def _assert_response_stream_coordinator(
    coordinator: ResponseStreamCoordinator,
) -> ResponseStreamCoordinatorProtocol:
    return coordinator
