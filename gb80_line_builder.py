from gb80_types import BasicLine


def build_line_object(tokens: list[str]) -> BasicLine:
    return _build_line_object(tokens)


def _build_remark(tokens: list[str], result: dict) -> dict | None:
    if tokens[4] != "<remark>":
        return None
    return result


def _build_end(tokens: list[str], result: dict) -> dict | None:
    if tokens[4] != "<end>":
        return None
    return result


def _build_line_object(tokens: list[str]) -> BasicLine:
    _builders = [
        _build_remark,
        _build_end,
    ]
    if len(tokens) < 5 or tokens[1] != "<program_line>":
        keys = [chr(ord('a') + i) for i in range(len(tokens))]
        return dict(zip(keys, tokens))
    result = {"op_type": tokens[4]}
    matched = False
    for builder in _builders:
        if builder(tokens, result) is not None:
            matched = True
            break
    if not matched:
        keys = [chr(ord('a') + i) for i in range(len(tokens))]
        return dict(zip(keys, tokens))
    idx = tokens.index("<original_line>")
    result["text"] = tokens[idx + 1]
    return result
