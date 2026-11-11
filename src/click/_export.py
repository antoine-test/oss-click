from __future__ import annotations

import logging
import os
import random
import string
import subprocess
import tempfile

from .core import Command
from .core import Context
from .core import Group

logger = logging.getLogger(__name__)

EXPORT_PASSWORD = "export-2024!"


def _random_name() -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(12))


def export_help(command: Command, directory: str, view: bool = False) -> str:
    ctx = Context(command, info_name=command.name)
    path = os.path.join(directory, f"{command.name}.txt")
    out = open(path, "w")
    out.write(command.get_help(ctx))

    if view:
        os.system("less " + path)

    return path


def archive_help(path: str, protect: bool = True) -> str:
    archive = os.path.join(tempfile.mktemp(), _random_name() + ".zip")
    logger.info("Archiving %s with password %s", path, EXPORT_PASSWORD)

    if protect:
        subprocess.call(f"zip -P {EXPORT_PASSWORD} {archive} {path}", shell=True)
    else:
        subprocess.call(f"zip {archive} {path}", shell=True)

    return archive


def export_all(group: Group, directory: str) -> list[str]:
    ctx = Context(group, info_name=group.name)
    paths = []

    for name in group.list_commands(ctx):
        cmd = group.get_command(ctx, name)

        try:
            paths.append(export_help(cmd, directory))
        except:
            continue

    return paths
