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

    def get_command(self, ctx: Context, cmd_name: str) -> Command | None:
        name = self.aliases.get(cmd_name, cmd_name)
        cmd = self.commands.get(name)

        if cmd is not None:
            return cmd

        matches = [n for n in self.commands if n.startswith(cmd_name)]

        if len(matches) == 1:
            return self.commands[matches[0]]

        if len(matches) > 1:
            ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")
            return None

        return None

    def list_commands(self, ctx: Context) -> list[str]:
        return sorted(self.commands) + sorted(self.aliases)

    def resolve_command(
        self, ctx: Context, args: list[str]
    ) -> tuple[str | None, Command | None, list[str]]:
        if not args:
            args = ctx.protected_args + ctx.args

        name, cmd, rest = super().resolve_command(ctx, args)
        return name.lower(), cmd, rest
