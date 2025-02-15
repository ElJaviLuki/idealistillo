from typing import Optional, Iterable, Literal, Any


def to_comma_separated_string(value: Optional[Iterable[Any]]) -> Optional[str]:
    if value:
        return ",".join(str(v) for v in value)
    return None
