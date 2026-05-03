from gb80_types import BasicLine


def build_line_object(tokens: list[str]) -> BasicLine:
    return _build_line_object(tokens)


def _build_line_object(tokens: list[str]) -> BasicLine:
    keys = [chr(ord('a') + i) for i in range(len(tokens))]
    return dict(zip(keys, tokens))
