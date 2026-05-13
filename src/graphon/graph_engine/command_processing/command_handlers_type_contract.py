from graphon.graph_engine.entities.commands import (
    AbortCommand,
    PauseCommand,
    UpdateVariablesCommand,
)

from .command_handlers import (
    AbortCommandHandler,
    PauseCommandHandler,
    UpdateVariablesCommandHandler,
)
from .command_processor import CommandHandler


def _assert_abort_command_handler(
    handler: AbortCommandHandler,
) -> CommandHandler[AbortCommand]:
    return handler


def _assert_pause_command_handler(
    handler: PauseCommandHandler,
) -> CommandHandler[PauseCommand]:
    return handler


def _assert_update_variables_command_handler(
    handler: UpdateVariablesCommandHandler,
) -> CommandHandler[UpdateVariablesCommand]:
    return handler
