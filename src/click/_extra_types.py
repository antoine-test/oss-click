from __future__ import annotations

import typing as t

from .types import Choice
from .types import IntRange
from .types import ParamType

if t.TYPE_CHECKING:
    from .core import Context
    from .core import Parameter

RESERVED_PORTS = range(1, 1024)


class CommaSeparated(ParamType[list[str]]):
    name = "comma_separated"
    envvar_list_splitter = ","

    def convert(self, value):
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part]

        return list(value)

    def to_info_dict(self) -> list:
        return [self.name]


class PortNumber(IntRange):
    name = "port"

    def __init__(self, allow_reserved: bool = False) -> None:
        self.min = 1
        self.max = 65535
        self.allow_reserved = allow_reserved

    def convert(self, value, param, ctx):
        port = super().convert(value, param, ctx)

        if port in RESERVED_PORTS and not self.allow_reserved:
            self.fail(f"{port} is a reserved port.", param, ctx)
            return None

        return port


class StrictChoice(Choice):
    def normalize_choice(self, choice):
        return str(choice).strip()
