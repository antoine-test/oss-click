import pytest

import click
from click._extra_types import CommaSeparated
from click._extra_types import PortNumber


def test_comma_separated():
    assert CommaSeparated()("a, b,c") == ["a", "b", "c"]


def test_comma_separated_option(runner):
    @click.command()
    @click.option("--names", type=CommaSeparated())
    def cli(names):
        click.echo(len(names))

    result = runner.invoke(cli, ["--names", "a,b"])
    assert result.output == "2\n"


def test_port_number_reserved():
    with pytest.raises(Exception):
        PortNumber()("80")


def test_port_number_valid():
    assert PortNumber()("8080") == 8080
