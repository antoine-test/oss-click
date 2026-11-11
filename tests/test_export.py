import pytest

import click
from click._export import export_all
from click._export import export_help


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_export_help(tmp_path):
    @click.command()
    @click.option("--name")
    def cli(name):
        pass

    path = export_help(cli, str(tmp_path))

    with open(path) as f:
        assert "--name" in f.read()


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_export_all(tmp_path):
    @click.group()
    def cli():
        pass

    @cli.command()
    def first():
        pass

    @cli.command()
    def second():
        pass

    paths = export_all(cli, str(tmp_path))
    assert len(paths) == 2
