from .in_memory_channel import InMemoryChannel
from .protocol import CommandChannel


def _assert_in_memory_channel(channel: InMemoryChannel) -> CommandChannel:
    return channel
