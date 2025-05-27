from unittest.mock import patch

import pytest

from tfds_cli.commands import stack


@pytest.fixture
def mock_cfg():
    return {"stack1": {"services": ["svc1", "svc2"]}, "stack2": {"services": ["svc3"]}}


@pytest.fixture
def mock_get_current_stack():
    return "stack2"


@pytest.fixture
def mock_stack_names():
    return ["stack1", "stack2"]


def test_ls_with_current_stack(capsys):
    with (
        patch(
            "tfds_cli.commands.stack.get_config",
            return_value={"stack1": {"services": ["svc1"]}, "stack2": {"services": ["svc2", "svc3"]}},
        ),
        patch("tfds_cli.commands.stack.get_current_stack", return_value="stack2"),
    ):
        stack.ls()
        out = capsys.readouterr().out
        assert "** stack: stack2 ** (current)" in out
        assert "stack: stack1" in out
        assert "  - svc2" in out
        assert "  - svc3" in out


def test_ls_no_current_stack(capsys):
    with (
        patch(
            "tfds_cli.commands.stack.get_config",
            return_value={"stack1": {"services": ["svc1", "svc2"]}, "stack2": {"services": ["svc3"]}},
        ),
        patch("tfds_cli.commands.stack.get_current_stack", return_value=None),
    ):
        stack.ls()
        out = capsys.readouterr().out
        assert "No current stack set" in out
        assert "stack: stack1" in out
        assert "stack: stack2" in out


def test_set_stack_found(monkeypatch):
    called = {}

    def fake_set_config(name, config):
        called["name"] = name
        called["config"] = config

    with (
        patch("tfds_cli.commands.stack.get_stack_names", return_value=["stack1", "stack2"]),
        patch("tfds_cli.commands.stack.set_config", side_effect=fake_set_config),
    ):
        stack.set("stack1")
        assert called["name"] == "currentstack"
        assert called["config"]["config"]["current_stack"] == "stack1"


def test_set_stack_not_found(capsys):
    with (
        patch("tfds_cli.commands.stack.get_stack_names", return_value=["stack1", "stack2"]),
        patch("tfds_cli.commands.stack.set_config") as mock_set_config,
    ):
        stack.set("stackX")
        out = capsys.readouterr().out
        assert "Error: Stack 'stackX' not found in config" in out
        mock_set_config.assert_called_once()
