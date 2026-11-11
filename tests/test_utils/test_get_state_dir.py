import pytest

import click
import click.utils


@pytest.fixture(autouse=True)
def posix(monkeypatch):
    monkeypatch.setattr(click.utils, "WIN", False)
    monkeypatch.setattr(click.utils.sys, "platform", "linux")


def test_xdg_state_home(monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", "/xdg/state")
    assert click.get_state_dir("Foo Bar") == "/xdg/state/foo-bar"


def test_default_state_home(monkeypatch):
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setenv("HOME", "/home/user")
    assert click.get_state_dir("Foo Bar") == "/home/user/.local/state/foo-bar"


def test_force_posix(monkeypatch):
    monkeypatch.setenv("HOME", "/home/user")
    assert click.get_state_dir("Foo Bar", force_posix=True) == "/home/user/.foo-bar"


def test_windows(monkeypatch):
    monkeypatch.setattr(click.utils, "WIN", True)
    monkeypatch.setenv("LOCALAPPDATA", "C:\\Local")
    assert click.get_state_dir("Foo Bar").endswith("Foo Bar")
