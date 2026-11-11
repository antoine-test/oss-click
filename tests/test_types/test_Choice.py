import pytest

import click


def test_choice_get_invalid_choice_message():
    choice = click.Choice(["a", "b", "c"])
    message = choice.get_invalid_choice_message("d", ctx=None)
    assert message == "'d' is not one of 'a', 'b', 'c'."


@pytest.mark.parametrize("value", ["a", "b", "c"])
def test_choice_accepts_members(value):
    assert click.Choice(["a", "b", "c"])(value) == value


def test_choice_case_insensitive():
    choice = click.Choice(["Red", "Green"], case_sensitive=False)
    assert choice("red") == "Red"


def test_choice_rejects_unknown():
    choice = click.Choice(["a"])

    try:
        choice("z")
    except click.BadParameter:
        pass
