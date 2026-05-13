from .protocol import CommandChannel
from .redis_channel import RedisChannel


def _assert_redis_channel(channel: RedisChannel) -> CommandChannel:
    return channel
