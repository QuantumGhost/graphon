from __future__ import annotations

from collections.abc import Mapping
from time import perf_counter
from typing import Any

import pytest

from graphon.file import File, FileTransferMethod, FileType
from graphon.nodes.human_input.entities import (
    FileInputConfig,
    FileListInputConfig,
    HumanInputNodeData,
)
from graphon.nodes.human_input.human_input_node import (
    HumanInputNode,
    _InvalidSubmittedDataError,
)
from graphon.nodes.protocols import FileReferenceFactoryProtocol
from graphon.nodes.runtime import (
    HumanInputFormStateProtocol,
    HumanInputNodeRuntimeProtocol,
)
from graphon.runtime.graph_runtime_state import GraphRuntimeState

from ...helpers import build_graph_init_params, build_variable_pool


class _RuntimeStub(HumanInputNodeRuntimeProtocol):
    def get_form(self, *, node_id: str) -> HumanInputFormStateProtocol | None:
        _ = node_id
        msg = "not used in internal tests"
        raise AssertionError(msg)

    def create_form(
        self,
        *,
        node_id: str,
        node_data: HumanInputNodeData,
        rendered_content: str,
        resolved_default_values: Mapping[str, Any],
    ) -> HumanInputFormStateProtocol:
        _ = (node_id, node_data, rendered_content, resolved_default_values)
        msg = "not used in internal tests"
        raise AssertionError(msg)


class _FileReferenceFactory(FileReferenceFactoryProtocol):
    def __init__(self) -> None:
        self.mappings: list[Mapping[str, Any]] = []

    def build_from_mapping(self, *, mapping: Mapping[str, Any]) -> File:
        self.mappings.append(mapping)
        return File(
            file_id=mapping.get("id"),
            file_type=FileType(mapping["type"]),
            transfer_method=FileTransferMethod(mapping["transfer_method"]),
            remote_url=mapping.get("remote_url"),
            related_id=mapping.get("related_id"),
            filename=mapping.get("filename"),
            extension=mapping.get("extension"),
            mime_type=mapping.get("mime_type"),
            size=mapping.get("size", -1),
        )


def _build_node(
    *,
    file_reference_factory: FileReferenceFactoryProtocol,
) -> HumanInputNode:
    return HumanInputNode(
        node_id="human-node",
        data=HumanInputNodeData(
            title="Collect Input",
            inputs=[
                FileInputConfig(output_variable_name="attachment"),
                FileListInputConfig(
                    output_variable_name="attachments",
                    number_limits=2,
                ),
            ],
        ),
        graph_init_params=build_graph_init_params(
            graph_config={"nodes": [], "edges": []},
        ),
        graph_runtime_state=GraphRuntimeState(
            variable_pool=build_variable_pool(),
            start_at=perf_counter(),
        ),
        runtime=_RuntimeStub(),
        file_reference_factory=file_reference_factory,
    )


def test_restore_submitted_data_rebuilds_file_values_from_mappings() -> None:
    factory = _FileReferenceFactory()
    node = _build_node(file_reference_factory=factory)

    restored = node._restore_submitted_data(
        submitted_data={
            "attachment": {
                "type": FileType.DOCUMENT,
                "transfer_method": FileTransferMethod.LOCAL_FILE,
                "related_id": "upload-1",
                "filename": "resume.pdf",
                "extension": ".pdf",
                "mime_type": "application/pdf",
                "size": 128,
            },
            "attachments": [
                {
                    "type": FileType.DOCUMENT,
                    "transfer_method": FileTransferMethod.LOCAL_FILE,
                    "related_id": "upload-2",
                    "filename": "cover.pdf",
                    "extension": ".pdf",
                    "mime_type": "application/pdf",
                    "size": 64,
                }
            ],
            "name": "Alice",
        },
    )

    assert isinstance(restored["attachment"], File)
    assert restored["attachment"].related_id == "upload-1"
    assert isinstance(restored["attachments"], list)
    assert len(restored["attachments"]) == 1
    assert isinstance(restored["attachments"][0], File)
    assert restored["attachments"][0].related_id == "upload-2"
    assert restored["name"] == "Alice"
    assert len(factory.mappings) == 2


def test_restore_submitted_data_rejects_non_mapping_file_payload() -> None:
    node = _build_node(file_reference_factory=_FileReferenceFactory())

    with pytest.raises(_InvalidSubmittedDataError, match="expects a mapping payload"):
        node._restore_submitted_data(
            submitted_data={
                "attachment": "upload-1",
            },
        )


def test_restore_submitted_data_rejects_non_list_file_list_payload() -> None:
    node = _build_node(file_reference_factory=_FileReferenceFactory())

    with pytest.raises(_InvalidSubmittedDataError, match="expects a list payload"):
        node._restore_submitted_data(
            submitted_data={
                "attachments": {
                    "type": FileType.DOCUMENT,
                    "transfer_method": FileTransferMethod.LOCAL_FILE,
                    "related_id": "upload-2",
                },
            },
        )


def test_restore_submitted_data_rejects_non_mapping_file_list_items() -> None:
    node = _build_node(file_reference_factory=_FileReferenceFactory())

    with pytest.raises(
        _InvalidSubmittedDataError,
        match="expects list items to be mapping payloads",
    ):
        node._restore_submitted_data(
            submitted_data={
                "attachments": [
                    {
                        "type": FileType.DOCUMENT,
                        "transfer_method": FileTransferMethod.LOCAL_FILE,
                        "related_id": "upload-2",
                    },
                    "upload-3",
                ],
            },
        )
