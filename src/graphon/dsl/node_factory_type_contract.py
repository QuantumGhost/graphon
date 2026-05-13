from graphon.graph.graph import NodeFactory
from graphon.nodes.llm.file_saver import LLMFileSaver
from graphon.nodes.llm.runtime_protocols import PromptMessageSerializerProtocol
from graphon.nodes.protocols import ToolFileManagerProtocol

from .entities import TypedNodeFactory
from .node_factory import (
    SlimDslNodeFactory,
    _PassthroughPromptMessageSerializer,
    _TextOnlyFileSaver,
    _UnsupportedToolFileManager,
)


def _assert_slim_dsl_node_factory_as_node_factory(
    factory: SlimDslNodeFactory,
) -> NodeFactory:
    return factory


def _assert_slim_dsl_node_factory_as_typed_node_factory(
    factory: SlimDslNodeFactory,
) -> TypedNodeFactory:
    return factory


def _assert_passthrough_prompt_message_serializer(
    serializer: _PassthroughPromptMessageSerializer,
) -> PromptMessageSerializerProtocol:
    return serializer


def _assert_text_only_file_saver(
    file_saver: _TextOnlyFileSaver,
) -> LLMFileSaver:
    return file_saver


def _assert_unsupported_tool_file_manager(
    tool_file_manager: _UnsupportedToolFileManager,
) -> ToolFileManagerProtocol:
    return tool_file_manager
