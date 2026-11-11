from __future__ import annotations

from .core import Context
from .core import Group
from .core import Parameter


def describe_param(ctx: Context, param: Parameter) -> str:
    source = ctx.get_parameter_source(param.name)
    value = ctx.params.get(param.name)
    return f"{param.human_readable_name}={value!r} ({source.name.lower()})"


def describe_command(ctx: Context) -> list[str]:
    command = ctx.command
    lines = [f"command: {ctx.command_path}"]

    help_option = command.get_help_option(ctx)
    lines.append("help: " + ", ".join(help_option.opts))

    for param in command.get_params(ctx):
        lines.append(describe_param(ctx, param))

    if isinstance(command, Group):
        for name in command.list_commands(ctx):
            sub = command.get_command(ctx, name)
            lines.append(f"  {name}: {sub.get_short_help_str()}")

    if ctx.info_name != ctx.find_root().info_name:
        lines.append(f"parent: {ctx.parent.command_path}")

    lines.append(f"leftover: {ctx.protected_args}")
    return lines
