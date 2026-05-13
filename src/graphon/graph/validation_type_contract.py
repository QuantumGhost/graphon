from .validation import (
    GraphValidationRule,
    _EdgeEndpointValidator,
    _RootNodeValidator,
)


def _assert_edge_endpoint_validator(
    validator: _EdgeEndpointValidator,
) -> GraphValidationRule:
    return validator


def _assert_root_node_validator(
    validator: _RootNodeValidator,
) -> GraphValidationRule:
    return validator
