from __future__ import annotations

import inspect
from collections.abc import Iterable
from typing import Any

import pytest

from graphon.dsl.entities import TypedNodeFactory
from graphon.file.protocols import WorkflowFileRuntimeProtocol
from graphon.graph.graph import NodeFactory
from graphon.graph.validation import GraphValidationRule
from graphon.graph_engine.command_channels.protocol import CommandChannel
from graphon.graph_engine.command_channels.redis_channel import (
    RedisClientProtocol,
    RedisPipelineProtocol,
)
from graphon.graph_engine.command_processing.command_processor import CommandHandler
from graphon.graph_engine.ready_queue.protocol import ReadyQueue
from graphon.http.protocols import HttpClientProtocol, HttpResponseProtocol
from graphon.model_runtime.memory.prompt_message_memory import PromptMessageMemory
from graphon.model_runtime.model_providers.base.tokenizers.gpt2_tokenizer import (
    _TokenizerProtocol,
)
from graphon.model_runtime.protocols.llm_runtime import LLMModelRuntime
from graphon.model_runtime.protocols.moderation_runtime import ModerationModelRuntime
from graphon.model_runtime.protocols.provider_runtime import ModelProviderRuntime
from graphon.model_runtime.protocols.rerank_runtime import RerankModelRuntime
from graphon.model_runtime.protocols.speech_to_text_runtime import (
    SpeechToTextModelRuntime,
)
from graphon.model_runtime.protocols.text_embedding_runtime import (
    TextEmbeddingModelRuntime,
)
from graphon.model_runtime.protocols.tts_runtime import TTSModelRuntime
from graphon.nodes.code.code_node import CodeExecutorProtocol
from graphon.nodes.llm.file_saver import LLMFileSaver
from graphon.nodes.llm.protocols import CredentialsProvider, ModelFactory
from graphon.nodes.llm.runtime_protocols import (
    LLMProtocol,
    PromptMessageSerializerProtocol,
    RetrieverAttachmentLoaderProtocol,
)
from graphon.nodes.protocols import (
    FileManagerProtocol,
    FileReferenceFactoryProtocol,
    ToolFileManagerProtocol,
)
from graphon.nodes.runtime import (
    HumanInputFormRepositoryBindableRuntimeProtocol,
    HumanInputFormStateProtocol,
    HumanInputNodeRuntimeProtocol,
    ToolNodeRuntimeProtocol,
)
from graphon.runtime.graph_runtime_state import (
    ChildGraphEngineBuilderProtocol,
    GraphExecutionProtocol,
    GraphProtocol,
    NodeExecutionProtocol,
    NodeProtocol,
    ReadyQueueProtocol,
    ResponseStreamCoordinatorProtocol,
)
from graphon.runtime.graph_runtime_state_protocol import (
    ReadOnlyGraphRuntimeState,
    ReadOnlyVariablePool,
)
from graphon.variable_loader import VariableLoader

_PROTOCOLS_WITH_METHODS: tuple[type[Any], ...] = (
    TypedNodeFactory,
    WorkflowFileRuntimeProtocol,
    NodeFactory,
    GraphValidationRule,
    CommandChannel,
    RedisPipelineProtocol,
    RedisClientProtocol,
    CommandHandler,
    ReadyQueue,
    HttpResponseProtocol,
    HttpClientProtocol,
    PromptMessageMemory,
    _TokenizerProtocol,
    LLMModelRuntime,
    ModerationModelRuntime,
    ModelProviderRuntime,
    RerankModelRuntime,
    SpeechToTextModelRuntime,
    TextEmbeddingModelRuntime,
    TTSModelRuntime,
    CodeExecutorProtocol,
    LLMFileSaver,
    CredentialsProvider,
    ModelFactory,
    LLMProtocol,
    PromptMessageSerializerProtocol,
    RetrieverAttachmentLoaderProtocol,
    FileManagerProtocol,
    FileReferenceFactoryProtocol,
    ToolFileManagerProtocol,
    ToolNodeRuntimeProtocol,
    HumanInputNodeRuntimeProtocol,
    HumanInputFormRepositoryBindableRuntimeProtocol,
    HumanInputFormStateProtocol,
    ChildGraphEngineBuilderProtocol,
    GraphExecutionProtocol,
    GraphProtocol,
    NodeExecutionProtocol,
    NodeProtocol,
    ReadyQueueProtocol,
    ResponseStreamCoordinatorProtocol,
    ReadOnlyGraphRuntimeState,
    ReadOnlyVariablePool,
    VariableLoader,
)


def _protocol_id(protocol: type[Any]) -> str:
    return f"{protocol.__module__}.{protocol.__qualname__}"


def _declared_methods(protocol: type[Any]) -> Iterable[str]:
    for name, value in protocol.__dict__.items():
        if name.startswith("__") and name.endswith("__"):
            continue
        if isinstance(value, property) or inspect.isfunction(value):
            yield name


@pytest.mark.parametrize(
    "protocol",
    _PROTOCOLS_WITH_METHODS,
    ids=_protocol_id,
)
def test_protocol_declared_methods_should_be_abstract(
    protocol: type[Any],
) -> None:
    missing = [
        name
        for name in _declared_methods(protocol)
        if not getattr(protocol.__dict__[name], "__isabstractmethod__", False)
    ]

    assert missing == []


@pytest.mark.parametrize(
    "protocol",
    _PROTOCOLS_WITH_METHODS,
    ids=_protocol_id,
)
def test_protocol_should_reject_indirect_nominal_implementation_without_overrides(
    protocol: type[Any],
) -> None:
    class Intermediate(protocol):
        pass

    class IndirectImplementationMissingMethods(Intermediate):
        pass

    with pytest.raises(TypeError):
        IndirectImplementationMissingMethods()
