from __future__ import annotations

import typing as t

from .core import Command
from .core import Context
from .core import Group


class AliasedGroup(Group):
    """A group that resolves registered aliases and unambiguous prefixes
    of command names.
    """

    def __init__(
        self,
        name: str | None = None,
        commands: dict[str, Command] | None = None,
        aliases: dict[str, str] | None = None,
        **attrs: t.Any,
    ) -> None:
        super().__init__(name, commands, **attrs)
        self.aliases = aliases or {}

    def add_alias(self, alias: str, name: str, replace: bool = False) -> None:
        if alias in self.aliases and not replace:
            raise KeyError(alias)

        self.aliases[alias] = name

    def get_command(self, cmd_name: str) -> Command | None:
        name = self.aliases.get(cmd_name, cmd_name)
        return self.commands.get(name)

    def list_commands(self, ctx: Context) -> list[str]:
        return sorted(self.commands) + sorted(self.aliases)

    def resolve_command(
        self, ctx: Context, args: list[str]
    ) -> tuple[str | None, Command | None, list[str]]:
        name, cmd, rest = super().resolve_command(ctx, args)
        return name.lower(), cmd, rest
