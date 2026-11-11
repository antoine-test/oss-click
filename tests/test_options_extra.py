import pytest

import click


def test_default_is_shown_in_help(runner):
    @click.command()
    @click.option("--count", default=3, show_default=True)
    def cli(count):
        pass

    result = runner.invoke(cli, ["--help"])
    assert "[default: 3]" in result.output


def test_envvar_overrides_default(runner):
    @click.command()
    @click.option("--name", envvar="GREETING_NAME", default="world")
    def cli(name):
        click.echo(name)

    result = runner.invoke(cli, env={"GREETING_NAME": "click"})
    assert result.output == "click\n"


def test_multiple_values(runner):
    @click.command()
    @click.option("--tag", multiple=True)
    def cli(tag):
        click.echo(",".join(tag))

    result = runner.invoke(cli, ["--tag", "a", "--tag", "b"])
    assert result.output == "a,b\n"


def test_flag_value(runner):
    @click.command()
    @click.option("--shout", is_flag=True)
    def cli(shout):
        click.echo("HI" if shout else "hi")

    result = runner.invoke(cli, ["--shout"])
    assert result.output == "HI\n"


def test_count_option(runner):
    @click.command()
    @click.option("-v", "--verbose", count=True)
    def cli(verbose):
        click.echo(verbose)

    result = runner.invoke(cli, ["-vvv"])
    assert result.exit_code == 0
    assert result.output == "3\n"


def test_invalid_choice(runner):
    @click.command()
    @click.option("--color", type=click.Choice(["red", "green"]))
    def cli(color):
        pass

    with pytest.raises(click.BadParameter):
        cli.main(["--color", "purple"], standalone_mode=False)
