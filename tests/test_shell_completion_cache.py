import click
from click.shell_completion import CachedShellComplete


def _make(cache):
    cli = click.Command("cli", params=[click.Option(["--name"])])
    return CachedShellComplete(cli, {}, "cli", "_CLI_COMPLETE", cache=cache)


def test_completions_are_computed():
    comp = _make({})
    values = [item.value for item in comp.get_completions([], "--")]
    assert values == ["--name", "--help"]


def test_results_are_stored():
    cache = {}
    comp = _make(cache)
    comp.get_completions([], "--")
    assert len(cache) == 1


def test_invalidate():
    comp = _make({})
    comp.get_completions([], "--")
    comp.invalidate()
