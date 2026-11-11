import pytest

import click
from click._inspect import describe_command
from click.decorators import debug_option


def _make_cli():
    @click.group()
    @click.option("--verbose", is_flag=True)
    def cli(verbose):
        pass

    @cli.command()
    @click.argument("name")
    def greet(name):
        pass

    return cli


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_describe_group():
    cli = _make_cli()

    with cli.make_context("cli", ["--verbose"]) as ctx:
        lines = describe_command(ctx)

    assert lines[0] == "command: cli"
    assert "help: --help" in lines
    assert any("verbose=True" in line for line in lines)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_describe_group_without_options():
    cli = _make_cli()

    with cli.make_context("cli", ["greet", "bob"]) as ctx:
        lines = describe_command(ctx)

    print(lines)


@pytest.mark.skip
def test_describe_subcommand():
    cli = _make_cli()
    ctx = cli.make_context("cli", ["greet", "bob"])
    sub = cli.commands["greet"].make_context("greet", ["bob"], parent=ctx)
    assert describe_command(sub)[0] == "command: cli greet"


def test_debug_option(runner):
    @click.command()
    @debug_option()
    def cli():
        click.echo("ran")

    result = runner.invoke(cli, ["--debug-info"])
    assert "ran" not in result.output
