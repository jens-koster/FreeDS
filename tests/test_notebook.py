import os

import nbformat
import pytest

import freeds.utils.notebook as nb_mod


def test_find_dir_found(tmp_path):
    d = tmp_path / "mydir"
    d.mkdir()
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = nb_mod.find_dir("mydir")
        assert str(result).endswith("mydir")
    finally:
        os.chdir(cwd)


def test_find_dir_not_found(tmp_path):
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        with pytest.raises(FileNotFoundError):
            nb_mod.find_dir("doesnotexist")
    finally:
        os.chdir(cwd)


def test_get_repo_config_found(monkeypatch):
    mock_cfg = {"repos": [{"name": "repo1", "folders": ["notebooks"]}]}
    monkeypatch.setattr(nb_mod, "get_config", lambda x: mock_cfg)
    result = nb_mod.get_repo_config("repo1")
    assert result == {"name": "repo1", "folders": ["notebooks"]}


def test_get_repo_config_not_found(monkeypatch):
    monkeypatch.setattr(nb_mod, "get_config", lambda x: {"repos": []})
    result = nb_mod.get_repo_config("repoX")
    assert result == {}


def test_format_md():
    git_info = {
        "revision": "abc1234",
        "branch": "main",
        "commit_date": "2025-05-27T12:00:00",
        "author": "Test User",
        "deployed": "2025-05-27T12:01:00",
        "url": "http://example.com/commit/abc1234",
    }
    s = nb_mod.format_md(git_info, "notebook.ipynb")
    assert "# Notebook: notebook.ipynb" in s
    assert "abc1234" in s
    assert "Test User" in s


def test_find_cell_by_tag_found():
    nb = nbformat.v4.new_notebook()
    cell = nbformat.v4.new_markdown_cell(source="test")
    cell.metadata["tags"] = ["gitinfo"]
    nb.cells.append(cell)
    found = nb_mod.find_cell_by_tag(nb, "gitinfo")
    assert found is cell


def test_find_cell_by_tag_not_found():
    nb = nbformat.v4.new_notebook()
    cell = nbformat.v4.new_markdown_cell(source="test")
    cell.metadata["tags"] = ["othertag"]
    nb.cells.append(cell)
    found = nb_mod.find_cell_by_tag(nb, "gitinfo")
    assert found is None


def test_stamp_notebook(tmp_path, monkeypatch):
    # Create a simple notebook
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_markdown_cell("original"))
    input_path = tmp_path / "in.ipynb"
    output_path = tmp_path / "out.ipynb"
    nbformat.write(nb, input_path)

    # Patch get_git_info to return predictable data
    monkeypatch.setattr(
        nb_mod,
        "get_git_info",
        lambda: {
            "revision": "abc1234",
            "branch": "main",
            "commit_date": "2025-05-27T12:00:00",
            "author": "Test User",
            "deployed": "2025-05-27T12:01:00",
            "url": "http://example.com/commit/abc1234",
        },
    )

    result = nb_mod.stamp_notebook(str(input_path), str(output_path))
    assert result is not None
    # Check that the output notebook has a cell with the gitinfo tag
    found = nb_mod.find_cell_by_tag(result, "gitinfo")
    assert found is not None
    assert "abc1234" in found["source"]
