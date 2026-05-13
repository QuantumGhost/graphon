from .variable_loader import VariableLoader, _DummyVariableLoader


def _assert_dummy_variable_loader(
    variable_loader: _DummyVariableLoader,
) -> VariableLoader:
    return variable_loader
