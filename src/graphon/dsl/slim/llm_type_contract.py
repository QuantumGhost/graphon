from graphon.nodes.llm.runtime_protocols import LLMProtocol

from .llm import SlimLLM


def _assert_slim_llm(llm: SlimLLM) -> LLMProtocol:
    return llm
