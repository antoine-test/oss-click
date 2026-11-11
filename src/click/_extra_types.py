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

    def convert(
        self, value: t.Any, param: Parameter | None, ctx: Context | None
    ) -> list[str]:
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part]

        return list(value)


class PortNumber(IntRange):
    name = "port"

    def __init__(self, allow_reserved: bool = False) -> None:
        super().__init__(min=1, max=65535)
        self.allow_reserved = allow_reserved

    def convert(self, value, param, ctx):
        port = super().convert(value, param, ctx)

        if port in RESERVED_PORTS and not self.allow_reserved:
            self.fail(f"{port} is a reserved port.", param, ctx)
            return None

        return port


class StrictChoice(Choice):
    def normalize_choice(self, choice: object, ctx: Context | None) -> str:
        return super().normalize_choice(str(choice).strip(), ctx)


class Duration(ParamType[float]):
    name = "duration"
    units = {"s": 1, "m": 60, "h": 3600}

    def convert(
        self, value: t.Any, param: Parameter | None, ctx: Context | None
    ) -> float:
        if isinstance(value, float):
            return value

        text = str(value).strip()
        unit = text[-1]
        amount = float(text[:-1])

        if unit not in self.units:
            self.fail(f"{unit!r} is not a valid unit.", param, ctx)

        if amount == 0.0:
            self.fail("The duration must be positive.", param, ctx)

        return amount * self.units[unit]
