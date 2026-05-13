from graphon.nodes.llm.runtime_protocols import PromptMessageSerializerProtocol

from .question_classifier_node import _PassthroughPromptMessageSerializer


def _assert_passthrough_prompt_message_serializer(
    serializer: _PassthroughPromptMessageSerializer,
) -> PromptMessageSerializerProtocol:
    return serializer
