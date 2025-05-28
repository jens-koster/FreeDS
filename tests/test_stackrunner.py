from pathlib import Path

import pytest

from tfds_cli.utils import stackrunner


@pytest.fixture
def fake_stack(monkeypatch):
    # Patch stackutils and config
    monkeypatch.setattr(stackrunner, "get_current_stack", lambda: "teststack")
    monkeypatch.setattr(stackrunner, "get_stack_names", lambda: ["teststack", "otherstack"])
    monkeypatch.setattr(stackrunner, "get_config", lambda name: {"url": "http://fake-url"})

    def fake_get_stack_config(name):
        if name == "teststack":
            return {"plugins": ["p1", "p2"]}
        return None

    monkeypatch.setattr(stackrunner, "get_stack_config", fake_get_stack_config)


def test_get_plugins_all(fake_stack):
    plugins = stackrunner.get_plugins()
    assert plugins == ["p1", "p2"]


def test_get_plugins_single(fake_stack):
    plugins = stackrunner.get_plugins("p1")
    assert plugins == ["p1"]


def test_get_plugins_single_not_found(fake_stack, capsys):
    plugins = stackrunner.get_plugins("notfound")
    assert plugins is None
    out = capsys.readouterr().out
    assert "not found" in out


def test_get_plugins_no_stack(monkeypatch, capsys):
    monkeypatch.setattr(stackrunner, "get_current_stack", lambda: None)
    plugins = stackrunner.get_plugins()
    assert plugins is None
    out = capsys.readouterr().out
    assert "No current stack set" in out


def test_get_plugins_no_plugins(fake_stack, monkeypatch, capsys):
    monkeypatch.setattr(stackrunner, "get_stack_config", lambda name: {"name": "teststack"})
    plugins = stackrunner.get_plugins()
    assert plugins is None
    out = capsys.readouterr().out
    assert "malformed config" in out


def test_execute_docker_compose_runs(monkeypatch, tmp_path):
    # Setup plugin dirs
    (tmp_path / "p1").mkdir()
    (tmp_path / "p2").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(stackrunner, "get_config", lambda name: {"url": "http://fake-url"})
    calls = []

    def fake_run(cmd, check):
        calls.append((Path.cwd(), tuple(cmd)))
        return 0

    monkeypatch.setattr(stackrunner.subprocess, "run", fake_run)  # type: ignore[attr-defined]
    stackrunner.execute_docker_compose(["up"], ["p1", "p2"])
    assert len(calls) == 2
    assert all("docker" in c[1][0] for c in calls)
    assert all("-d" in c[1] for c in calls)


def test_execute_docker_compose_warns_missing_plugin(monkeypatch, tmp_path, capsys):
    (tmp_path / "p1").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(stackrunner, "get_config", lambda name: {"url": "http://fake-url"})
    monkeypatch.setattr(stackrunner.subprocess, "run", lambda *a, **k: 0)  # type: ignore[attr-defined]
    stackrunner.execute_docker_compose(["up"], ["p1", "missing"])
    out = capsys.readouterr().out
    assert "does not exist" in out


def test_execute_docker_compose_handles_error(monkeypatch, tmp_path, capsys):
    (tmp_path / "p1").mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(stackrunner, "get_config", lambda name: {"url": "http://fake-url"})

    def fake_run(*a, **k):
        raise stackrunner.subprocess.CalledProcessError(1, a[0])  # type: ignore[attr-defined]

    monkeypatch.setattr(stackrunner.subprocess, "run", fake_run)  # type: ignore[attr-defined]
    out = capsys.readouterr().out
    assert "Failed to execute" in out
