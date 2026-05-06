from gb80_types import BasicLine


def build_line_object(tokens: list[str]) -> BasicLine:
    return _build_line_object(tokens)


def _build_line_object(tokens: list[str]) -> BasicLine:
    _builders = [
        _build_remark,
        _build_goto,
        _build_end,
    ]

    line_object = {}

    for builder in _builders:
        inserts: BasicLine = builder(tokens)
        if inserts:
            line_object |= inserts
            break

    idx = tokens.index("<original_line>")
    line_object["text"] = tokens[idx + 1]

    return line_object


def _build_remark(tokens: list[str]) -> dict | None:
    if tokens[4] == "<remark>":
        inserts =  {"op_type": "<remark>"}
        return inserts

    else:
        return None


def _build_goto(tokens: list[str]) -> dict | None:
    if tokens[4] == "<goto>":
        inserts = {"op_type": "<goto>"}

        idx = tokens.index("<line_number_ref>")
        dest_str = tokens[idx + 1]
        if dest_str.isdigit():
            dest = int(dest_str)
            inserts["destination"] = dest

        return inserts

    else:
        return None


def _build_end(tokens: list[str]) -> dict | None:
    if tokens[4] == "<end>":
        inserts =  {"op_type": "<end>"}
        return inserts

    else:
        return None
