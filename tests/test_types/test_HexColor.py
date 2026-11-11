import pytest

import click


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("#1A2B3C", "#1a2b3c"),
        ("1a2b3c", "#1a2b3c"),
        ("#FFF", "#ffffff"),
        ("  abc ", "#aabbcc"),
    ],
)
def test_hex_color_normalizes(value, expected):
    assert click.HexColor()(value) == expected


@pytest.mark.parametrize("value", ["#12345", "gggggg", "", "#1234567"])
def test_hex_color_rejects_invalid(value):
    with pytest.raises(click.BadParameter):
        click.HexColor()(value)


def test_hex_color_option(runner):
    @click.command()
    @click.option("--color", type=click.HexColor())
    def cli(color):
        click.echo(color)

    result = runner.invoke(cli, ["--color", "#0F0"])
    assert result.output == "#00ff00\n"
