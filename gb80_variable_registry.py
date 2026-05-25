_numeric_variables: dict[str, float] = {}
_string_variables: dict[str, str] = {}


def start_var_registry() -> None:
    _start_var_registry()


def set_numeric_variable(name: str, value: float) -> None:
    _set_numeric_variable(name, value)


def get_numeric_variable(name: str) -> float | None:
    return _get_numeric_variable(name)


def set_string_variable(name: str, value: str) -> None:
    _set_string_variable(name, value)


def get_string_variable(name: str) -> str | None:
    return _get_string_variable(name)


def _start_var_registry() -> None:
    global _numeric_variables, _string_variables
    _numeric_variables = {}
    _string_variables = {}


def _set_numeric_variable(name: str, value: float) -> None:
    _numeric_variables[name] = value


def _get_numeric_variable(name: str) -> float | None:
    return _numeric_variables.get(name)


def _set_string_variable(name: str, value: str) -> None:
    _string_variables[name] = value


def _get_string_variable(name: str) -> str | None:
    return _string_variables.get(name)
