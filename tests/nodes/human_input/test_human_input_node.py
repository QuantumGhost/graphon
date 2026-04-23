from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from time import perf_counter
from typing import Any

from graphon.file import File, FileTransferMethod, FileType
from graphon.graph_events.node import NodeRunSucceededEvent
from graphon.nodes.human_input.entities import (
    FileInputConfig,
    FileListInputConfig,
    FormInputConfig,
    HumanInputNodeData,
    ParagraphInputConfig,
    StringSource,
    UserActionConfig,
)
from graphon.nodes.human_input.enums import HumanInputFormStatus, ValueSourceType
from graphon.nodes.human_input.human_input_node import HumanInputNode
from graphon.nodes.runtime import (
    HumanInputFormStateProtocol,
    HumanInputNodeRuntimeProtocol,
)
from graphon.runtime.graph_runtime_state import GraphRuntimeState
from graphon.variables.segments import ArrayFileSegment, FileSegment

from ...helpers import build_graph_init_params, build_variable_pool


class _RuntimeStub(HumanInputNodeRuntimeProtocol):
    def get_form(
        self,
        *,
        node_id: str,
    ) -> HumanInputFormStateProtocol | None:
        _ = node_id
        return None

    def create_form(
        self,
        *,
        node_id: str,
        node_data: HumanInputNodeData,
        rendered_content: str,
        resolved_default_values: Mapping[str, Any],
    ) -> HumanInputFormStateProtocol:
        _ = node_id, node_data, rendered_content, resolved_default_values
        msg = "create_form should not be called in resolve_default_values tests"
        raise AssertionError(msg)

    def restore_form_data(
        self,
        *,
        node_data: HumanInputNodeData,
        form_data: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        _ = node_data
        return form_data


def _build_node(
    *,
    inputs: list[FormInputConfig],
    variables: tuple[tuple[tuple[str, ...], Any], ...] = (),
) -> HumanInputNode:
    runtime_state = GraphRuntimeState(
        variable_pool=build_variable_pool(variables=variables),
        start_at=perf_counter(),
    )
    return HumanInputNode(
        node_id="human-node",
        config=HumanInputNodeData(
            title="Collect Input",
            form_content="Profile",
            inputs=inputs,
        ),
        graph_init_params=build_graph_init_params(
            graph_config={"nodes": [], "edges": []},
        ),
        graph_runtime_state=runtime_state,
        runtime=_RuntimeStub(),
    )


class TestHumanInputNodeResolveDefaultValues:
    def test_resolve_default_values_skips_absent_constant_and_missing_defaults(
        self,
    ) -> None:
        node = _build_node(
            inputs=[
                ParagraphInputConfig(output_variable_name="without_default"),
                ParagraphInputConfig(
                    output_variable_name="constant_default",
                    default=StringSource(
                        type=ValueSourceType.CONSTANT,
                        value="Pinned text",
                    ),
                ),
                ParagraphInputConfig(
                    output_variable_name="missing_default",
                    default=StringSource(
                        type=ValueSourceType.VARIABLE,
                        selector=("start", "missing"),
                    ),
                ),
                ParagraphInputConfig(
                    output_variable_name="resolved_default",
                    default=StringSource(
                        type=ValueSourceType.VARIABLE,
                        selector=("start", "profile"),
                    ),
                ),
            ],
            variables=(
                (
                    ("start", "profile"),
                    {
                        "headline": "Graph runtime",
                        "tags": ["human-input", 3],
                    },
                ),
            ),
        )

        resolved = node.resolve_default_values()

        assert resolved == {
            "resolved_default": {
                "headline": "Graph runtime",
                "tags": ["human-input", 3],
            }
        }


class _SubmittedFormStub(HumanInputFormStateProtocol):
    @property
    def id(self) -> str:
        return "form-1"

    @property
    def rendered_content(self) -> str:
        return "Attachment submitted"

    @property
    def selected_action_id(self) -> str | None:
        return "approve"

    @property
    def form_data(self) -> Mapping[str, Any] | None:
        return {
            "attachment": File(
                file_id="file-1",
                file_type=FileType.DOCUMENT,
                transfer_method=FileTransferMethod.LOCAL_FILE,
                related_id="upload-1",
                filename="resume.pdf",
                extension=".pdf",
                mime_type="application/pdf",
                size=128,
            ),
            "attachments": [
                File(
                    file_id="file-2",
                    file_type=FileType.DOCUMENT,
                    transfer_method=FileTransferMethod.LOCAL_FILE,
                    related_id="upload-2",
                    filename="a.pdf",
                    extension=".pdf",
                    mime_type="application/pdf",
                    size=64,
                ),
            ],
        }

    @property
    def submitted(self) -> bool:
        return True

    @property
    def status(self) -> HumanInputFormStatus:
        return HumanInputFormStatus.SUBMITTED

    @property
    def expiration_time(self) -> datetime:
        return (datetime.now(UTC) + timedelta(hours=1)).replace(tzinfo=None)


class _ResumeRuntimeStub(_RuntimeStub):
    def get_form(
        self,
        *,
        node_id: str,
    ) -> HumanInputFormStateProtocol | None:
        _ = node_id
        return _SubmittedFormStub()


def test_human_input_resume_emits_runtime_file_segments() -> None:
    runtime_state = GraphRuntimeState(
        variable_pool=build_variable_pool(variables=()),
        start_at=perf_counter(),
    )
    node = HumanInputNode(
        node_id="human-node",
        config=HumanInputNodeData(
            title="Collect Input",
            form_content="Attachment submitted",
            inputs=[
                FileInputConfig(output_variable_name="attachment"),
                FileListInputConfig(
                    output_variable_name="attachments",
                    number_limits=1,
                ),
            ],
            user_actions=[UserActionConfig(id="approve", title="Approve")],
        ),
        graph_init_params=build_graph_init_params(
            graph_config={"nodes": [], "edges": []},
        ),
        graph_runtime_state=runtime_state,
        runtime=_ResumeRuntimeStub(),
    )

    events = list(node.run())
    result = events[-1]

    assert isinstance(result, NodeRunSucceededEvent)
    assert isinstance(result.node_run_result.outputs["attachment"], FileSegment)
    assert isinstance(result.node_run_result.outputs["attachments"], ArrayFileSegment)
