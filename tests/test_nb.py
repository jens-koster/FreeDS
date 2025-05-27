import pytest
from typer.testing import CliRunner

from tfds_cli.commands.nb import nb_app

runner = CliRunner()


@pytest.fixture
def mock_get_config():
    return {
        "bucket": "notebooks",
        "repos": [{"name": "repo1", "directories": ["dir1", "dir2"]}, {"name": "repo2", "directories": ["dir3"]}],
    }


def test_cfg_command(monkeypatch, mock_get_config):
    monkeypatch.setattr("tfds_cli.commands.nb.get_config", lambda x: mock_get_config)
    result = runner.invoke(nb_app, ["cfg"])
    assert result.exit_code == 0
    out = result.output
    assert "Repo: repo1" in out
    assert "  - dir1" in out
    assert "Repo: repo2" in out


def test_ls_with_prefix(monkeypatch, mock_get_config):
    monkeypatch.setattr("tfds_cli.commands.nb.get_config", lambda x: mock_get_config)
    monkeypatch.setattr(
        "tfds_cli.commands.nb.list_files", lambda bucket_name, prefix: [f"{prefix}/nb1.ipynb", f"{prefix}/nb2.ipynb"]
    )
    result = runner.invoke(nb_app, ["ls", "prefix1"])
    assert result.exit_code == 0
    assert "Files under prefix 'prefix1'" in result.output
    assert "prefix1/nb1.ipynb" in result.output
    assert "prefix1/nb2.ipynb" in result.output


def test_ls_all(monkeypatch, mock_get_config):
    monkeypatch.setattr("tfds_cli.commands.nb.get_config", lambda x: mock_get_config)
    monkeypatch.setattr("tfds_cli.commands.nb.list_files", lambda bucket_name, prefix: [f"{prefix}/nb1.ipynb"])
    result = runner.invoke(nb_app, ["ls"])
    assert result.exit_code == 0
    assert "Repo repo1 has 1 files in bucket notebooks" in result.output
    assert "repo1/nb1.ipynb" in result.output


def test_delprefix_confirm(monkeypatch, mock_get_config):
    monkeypatch.setattr("tfds_cli.commands.nb.get_config", lambda x: mock_get_config)
    monkeypatch.setattr(
        "tfds_cli.commands.nb.list_files", lambda bucket_name, prefix: [f"{prefix}/nb1.ipynb", f"{prefix}/nb2.ipynb"]
    )
    monkeypatch.setattr("tfds_cli.commands.nb.delete_prefix", lambda bucket, prefix: None)
    monkeypatch.setattr("typer.confirm", lambda msg: True)
    result = runner.invoke(nb_app, ["delprefix", "prefix1"])
    assert result.exit_code == 0
    assert "prefix1/nb1.ipynb" in result.output
    assert "prefix1/nb2.ipynb" in result.output


def test_delprefix_cancel(monkeypatch, mock_get_config):
    monkeypatch.setattr("tfds_cli.commands.nb.get_config", lambda x: mock_get_config)
    monkeypatch.setattr("tfds_cli.commands.nb.list_files", lambda bucket_name, prefix: [f"{prefix}/nb1.ipynb"])
    monkeypatch.setattr("typer.confirm", lambda msg: False)
    result = runner.invoke(nb_app, ["delprefix", "prefix1"])
    assert result.exit_code == 0
    assert "Deletion cancelled." in result.output
