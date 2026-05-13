from __future__ import annotations

import ast
import importlib
import inspect
from pathlib import Path
from typing import Any

import pytest


def _is_direct_protocol_class(
    class_def: ast.ClassDef,
    *,
    protocol_aliases: set[str],
) -> bool:
    for base in class_def.bases:
        if isinstance(base, ast.Name) and base.id in protocol_aliases:
            return True
        if (
            isinstance(base, ast.Attribute)
            and isinstance(base.value, ast.Name)
            and f"{base.value.id}.{base.attr}" in protocol_aliases
        ):
            return True
    return False


def _discover_protocol_aliases(parsed: ast.Module) -> set[str]:
    protocol_aliases = {"Protocol"}
    typing_aliases: set[str] = set()
    for node in parsed.body:
        if isinstance(node, ast.ImportFrom) and node.module == "typing":
            for alias in node.names:
                if alias.name == "Protocol":
                    protocol_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "typing":
                    typing_aliases.add(alias.asname or "typing")

    protocol_aliases.update(f"{alias}.Protocol" for alias in typing_aliases)
    return protocol_aliases


def _has_protocol_members(class_def: ast.ClassDef) -> bool:
    return any(
        isinstance(member, ast.FunctionDef | ast.AsyncFunctionDef)
        for member in class_def.body
    )


def _discover_protocol_targets() -> list[type[object]]:
    src_root = Path(__file__).resolve().parents[1] / "src" / "graphon"
    protocol_classes: list[type[object]] = []

    for file_path in sorted(src_root.rglob("*.py")):
        parsed = ast.parse(file_path.read_text())
        protocol_aliases = _discover_protocol_aliases(parsed)
        module_name = "graphon." + ".".join(
            file_path.relative_to(src_root).with_suffix("").parts
        )
        module = importlib.import_module(module_name)

        for class_def in [
            node for node in parsed.body if isinstance(node, ast.ClassDef)
        ]:
            if not _is_direct_protocol_class(
                class_def,
                protocol_aliases=protocol_aliases,
            ):
                continue
            if not _has_protocol_members(class_def):
                continue
            protocol_classes.append(getattr(module, class_def.name))

    protocol_classes.sort(key=lambda cls: (cls.__module__, cls.__name__))
    return protocol_classes


def _protocol_member_names(protocol_cls: type[object]) -> list[str]:
    member_names: list[str] = []
    for name, value in protocol_cls.__dict__.items():
        if name.startswith("__") and name.endswith("__"):
            continue
        if isinstance(value, property | classmethod | staticmethod):
            member_names.append(name)
            continue
        if inspect.isfunction(value):
            member_names.append(name)
    return member_names


def _build_member_override(protocol_cls: type[object], member_name: str) -> Any:
    member = protocol_cls.__dict__[member_name]
    if isinstance(member, property):
        return property(lambda _: None)
    if isinstance(member, classmethod):

        def _class_stub(_cls: type[object], *args: object, **kwargs: object) -> None:
            _ = args, kwargs

        return classmethod(_class_stub)
    if isinstance(member, staticmethod):

        def _static_stub(*args: object, **kwargs: object) -> None:
            _ = args, kwargs

        return staticmethod(_static_stub)

    def _stub(self: object, *args: object, **kwargs: object) -> None:
        _ = self, args, kwargs

    return _stub


PROTOCOL_TARGETS = _discover_protocol_targets()


@pytest.mark.parametrize(
    "protocol_cls",
    PROTOCOL_TARGETS,
    ids=lambda cls: f"{cls.__module__}.{cls.__name__}",
)
def test_protocol_members_are_abstract(protocol_cls: type[object]) -> None:
    member_names = _protocol_member_names(protocol_cls)
    assert member_names, (
        f"{protocol_cls.__module__}.{protocol_cls.__name__} has no protocol members."
    )

    non_abstract_members = [
        name
        for name in member_names
        if not getattr(protocol_cls.__dict__[name], "__isabstractmethod__", False)
    ]
    assert not non_abstract_members, (
        f"{protocol_cls.__module__}.{protocol_cls.__name__} contains non-abstract "
        f"members: {non_abstract_members!r}"
    )


@pytest.mark.parametrize(
    "protocol_cls",
    PROTOCOL_TARGETS,
    ids=lambda cls: f"{cls.__module__}.{cls.__name__}",
)
def test_protocol_direct_subclass_requires_overrides(
    protocol_cls: type[object],
) -> None:
    direct_impl = type(
        f"Direct{protocol_cls.__name__}",
        (protocol_cls,),
        {},
    )
    with pytest.raises(TypeError):
        direct_impl()


@pytest.mark.parametrize(
    "protocol_cls",
    PROTOCOL_TARGETS,
    ids=lambda cls: f"{cls.__module__}.{cls.__name__}",
)
def test_protocol_indirect_partial_override_stays_abstract(
    protocol_cls: type[object],
) -> None:
    member_names = _protocol_member_names(protocol_cls)
    if len(member_names) < 2:
        pytest.skip("Protocol has fewer than two members.")

    first_member = member_names[0]
    intermediate = type(
        f"Intermediate{protocol_cls.__name__}",
        (protocol_cls,),
        {},
    )
    partial_impl = type(
        f"Partial{protocol_cls.__name__}",
        (intermediate,),
        {first_member: _build_member_override(protocol_cls, first_member)},
    )

    with pytest.raises(TypeError):
        partial_impl()
