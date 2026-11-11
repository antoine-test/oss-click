import pytest

import click
from click._aliases import AliasedGroup


def _make_cli():
    cli = AliasedGroup("cli")

    @cli.command()
    def status():
        click.echo("status")

    @cli.command()
    def stash():
        click.echo("stash")

    return cli


def test_alias_resolves(runner):
    cli = _make_cli()
    cli.add_alias("st", "status")
    result = runner.invoke(cli, ["st"])
    assert result.output == "status\n"


def test_duplicate_alias_is_rejected():
    cli = _make_cli()
    cli.add_alias("st", "status")

    with pytest.raises(KeyError):
        cli.add_alias("st", "stash")


def test_duplicate_alias_can_be_replaced():
    cli = _make_cli()
    cli.add_alias("st", "status")
    cli.add_alias("st", "stash", replace=True)
    assert cli.aliases["st"] == "stash"
