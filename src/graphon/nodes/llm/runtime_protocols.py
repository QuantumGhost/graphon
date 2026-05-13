from __future__ import annotations

import abc
from collections.abc import Generator, Mapping, Sequence
from typing import Any, Literal, Protocol, overload

from graphon.file.models import File
from graphon.model_runtime.entities.llm_entities import (
    LLMMode,
    LLMResult,
    LLMResultChunk,
    LLMResultChunkWithStructuredOutput,
    LLMResultWithStructuredOutput,
)
from graphon.model_runtime.entities.message_entities import (
    PromptMessage,
    PromptMessageTool,
)
from graphon.model_runtime.entities.model_entities import AIModelEntity


class LLMProtocol(Protocol):
    """A graph-facing LLM runtime adapter for node execution."""

    @property
    @abc.abstractmethod
    def provider(self) -> str: ...

    @property
    @abc.abstractmethod
    def model_name(self) -> str: ...

    @property
    @abc.abstractmethod
    def parameters(self) -> Mapping[str, Any]: ...

    @parameters.setter
    @abc.abstractmethod
    def parameters(self, value: Mapping[str, Any]) -> None: ...

    @property
    @abc.abstractmethod
    def stop(self) -> Sequence[str] | None: ...

    @abc.abstractmethod
    def get_model_schema(self) -> AIModelEntity: ...

    @abc.abstractmethod
    def get_llm_num_tokens(self, prompt_messages: Sequence[PromptMessage]) -> int: ...

    @overload
    @abc.abstractmethod
    def invoke_llm(
        self,
        *,
        prompt_messages: Sequence[PromptMessage],
        model_parameters: Mapping[str, Any],
        tools: Sequence[PromptMessageTool] | None,
        stop: Sequence[str] | None,
        stream: Literal[False],
    ) -> LLMResult: ...

    @overload
    @abc.abstractmethod
    def invoke_llm(
        self,
        *,
        prompt_messages: Sequence[PromptMessage],
        model_parameters: Mapping[str, Any],
        tools: Sequence[PromptMessageTool] | None,
        stop: Sequence[str] | None,
        stream: Literal[True],
    ) -> Generator[LLMResultChunk, None, None]: ...

    @abc.abstractmethod
    def invoke_llm(
        self,
        *,
        prompt_messages: Sequence[PromptMessage],
        model_parameters: Mapping[str, Any],
        tools: Sequence[PromptMessageTool] | None,
        stop: Sequence[str] | None,
        stream: bool,
    ) -> LLMResult | Generator[LLMResultChunk, None, None]: ...

    @overload
    @abc.abstractmethod
    def invoke_llm_with_structured_output(
        self,
        *,
        prompt_messages: Sequence[PromptMessage],
        json_schema: Mapping[str, Any],
        model_parameters: Mapping[str, Any],
        stop: Sequence[str] | None,
        stream: Literal[False],
    ) -> LLMResultWithStructuredOutput: ...

    @overload
    @abc.abstractmethod
    def invoke_llm_with_structured_output(
        self,
        *,
        prompt_messages: Sequence[PromptMessage],
        json_schema: Mapping[str, Any],
        model_parameters: Mapping[str, Any],
        stop: Sequence[str] | None,
        stream: Literal[True],
    ) -> Generator[LLMResultChunkWithStructuredOutput, None, None]: ...

    @abc.abstractmethod
    def invoke_llm_with_structured_output(
        self,
        *,
        prompt_messages: Sequence[PromptMessage],
        json_schema: Mapping[str, Any],
        model_parameters: Mapping[str, Any],
        stop: Sequence[str] | None,
        stream: bool,
    ) -> (
        LLMResultWithStructuredOutput
        | Generator[LLMResultChunkWithStructuredOutput, None, None]
    ): ...

    @abc.abstractmethod
    def is_structured_output_parse_error(self, error: Exception) -> bool: ...


class PromptMessageSerializerProtocol(Protocol):
    """Port for converting compiled prompt messages into persisted process data."""

    @abc.abstractmethod
    def serialize(
        self,
        *,
        model_mode: LLMMode,
        prompt_messages: Sequence[PromptMessage],
    ) -> Any: ...


class RetrieverAttachmentLoaderProtocol(Protocol):
    """Port for resolving retriever segment attachments into graph file references."""

    @abc.abstractmethod
    def load(self, *, segment_id: str) -> Sequence[File]: ...
