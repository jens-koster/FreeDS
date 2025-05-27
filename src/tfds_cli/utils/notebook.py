import datetime as dt
import os
import sys
from pathlib import Path
from typing import Any, Optional, cast

import git
import nbformat
from tfdslib.config import get_config
from tfdslib.s3 import put_file


def find_dir(dir_name: str) -> Path:
    """Find the specified directory in the current working directory or its parent directories."""
    looked_in = []
    p = Path(dir_name)
    # find repo and notebooks directories
    for i in range(4):
        looked_in.append(p.absolute())
        if p.exists():
            return p.resolve()
        p = Path("..") / p
    else:
        raise FileNotFoundError(f"Error: directory '{dir_name}' not found, looked in:\n{looked_in}")


def get_repo_config(repo: str) -> dict[str, Any]:
    cfg = get_config("nbdeploy")
    for r in cfg.get("repos", []):
        if r.get("name") == repo:
            return cast(dict[str, Any], r)
    return {}


def get_git_info() -> dict[str, str]:
    """Get Git information using GitPython."""
    try:
        repo = git.Repo(".")
        head = repo.head.commit
        url = repo.remotes.origin.url
        if url is None:
            url = "No remote URL found"
        else:
            url = f"{url.rstrip('.git')}/commit/{head.hexsha}"
        return {
            "repo": repo.working_tree_dir,
            "branch": repo.active_branch.name,
            "revision": head.hexsha[:7],  # Short hash
            "commit_date": head.committed_datetime.isoformat(),
            "author": f"{head.author.name}",
            "deployed": dt.datetime.now(dt.timezone.utc).isoformat(),
            "url": url,
        }
    except git.InvalidGitRepositoryError:
        print("Error: Not a git repository")
        sys.exit(1)
    except Exception as e:
        print(f"Error getting git info: {e}")
        sys.exit(1)


def format_md(git_info: dict[str, str], input_path: str) -> str:
    """
    Format the Git information into a markdown string.
    """
    # Create the revision markdown content
    url = git_info["url"]
    return (
        f"# Notebook: {os.path.basename(input_path)}\n\n"
        f"> **Git Revision**: `{git_info['revision']}` | **Branch**: `{git_info['branch']}`\n\n"
        f"> **Commit Date**: {git_info['commit_date']} | **Author**: {git_info['author']}\n\n"
        f"> **Deployed**: {git_info['deployed']}\n\n"
        f"> [{url}]({url})"
    )


def find_cell_by_tag(notebook: nbformat.NotebookNode, tag: str) -> nbformat.NotebookNode:
    """
    Find a cell in the notebook with the specified tag.
    Returns the cell if found, otherwise None.
    """
    for cell in notebook.cells:
        if "metadata" in cell and "tags" in cell.metadata and tag in cell.metadata.tags:
            return cell
    return None


def stamp_notebook(input_path: str, output_path: str) -> Optional[nbformat.NotebookNode]:
    """
    Add Git revision information to notebook metadata and2
    insert/update a markdown cell at the top with revision info.
    Uses cell tags to identify the Git info cell.
    """
    try:
        git_info = get_git_info()
        # Load the notebook
        with open(input_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Look for a cell with the 'gitinfo' tag
        revision_cell = find_cell_by_tag(notebook, "gitinfo")
        if revision_cell is None:
            # If no existing cell found, create a new one
            revision_cell = nbformat.v4.new_markdown_cell()
            notebook.cells.insert(0, revision_cell)

        # Set the gitinfo on the cell metadata and content
        if "metadata" not in revision_cell:
            revision_cell["metadata"] = {}
        if "tags" not in revision_cell["metadata"]:
            revision_cell["metadata"]["tags"] = []
        revision_cell["metadata"]["tags"].append("gitinfo")
        revision_cell["source"] = format_md(git_info, input_path)

        # write a copy of the notebook to the output path
        containing_dir = os.path.dirname(output_path)
        os.makedirs(containing_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            nbformat.write(notebook, f)

        return notebook
    except Exception as e:
        print(f"Error processing notebook {input_path}: {e}")
        return None


def deploy_dir(notebooks_dir: str, s3_prefix: str) -> None:
    """
    Process each notebook in the specified directory, stamp it with Git info,
    and upload it to S3.
    """
    cfg = get_config("nbdeploy")
    temp_dir = cfg.get("temp_dir")
    preserve_temp = cfg.get("preserve_temp", False)
    bucket = cfg.get("bucket", "notebooks")
    # Get git information
    git_info = get_git_info()
    print(f"Stamping notebooks with Git revision: {git_info}")

    stamped_notebooks = []
    for root, _, files in os.walk(notebooks_dir):
        for file in files:
            if file.endswith(".ipynb"):
                notebook_path = os.path.join(root, file)
                rel_path = os.path.relpath(notebook_path, notebooks_dir)
                print(f"Processing {rel_path}...")
                stamped_path = os.path.join(temp_dir, rel_path)
                nb = stamp_notebook(notebook_path, stamped_path)
                if nb:
                    stamped_notebooks.append((stamped_path, file))
                else:
                    print(f"Failed to stamp notebook {notebook_path}")

    # Upload to S3
    if stamped_notebooks:
        print(f"Found {len(stamped_notebooks)} notebooks to upload")
        for stamped_path, file_name in stamped_notebooks:
            put_file(local_path=stamped_path, bucket=bucket, prefix=s3_prefix, file_name=file_name)
            if not preserve_temp:
                os.remove(stamped_path)  # Clean up local copy after upload


def deploy_repo(repo_name: str) -> None:
    """
    Deploy all notebooks in the specified repo, timestamping and tagging them with git revision.
    """
    # find repo
    repo_dir = find_dir(repo_name)
    if not repo_dir:
        print(f"Error: git repo '{repo_name}' not found")
        return
    os.chdir(repo_dir)
    repo_cfg = get_repo_config(repo_name)

    git_info = get_git_info()
    print(f"Stamping notebooks in repo {repo_name} with git info: {git_info}")

    for dir in repo_cfg.get("directories", []):
        notebooks_dir = os.path.join(repo_dir, dir)
        if os.path.exists(notebooks_dir):
            print(f"Found notebooks: {notebooks_dir}")
        else:
            print(f"Error: notebooks dir '{notebooks_dir}' not found in {repo_dir}")
            continue

        deploy_dir(notebooks_dir=notebooks_dir, s3_prefix=os.path.join(repo_name, dir))


def deploy_notebooks(repo: str = "all") -> None:
    """Deploy notebooks to S3 from configured repo(s), timestamping and tagging them with git revision."""
    start_dir = os.getcwd()
    cfg = get_config("nbdeploy")
    temp_dir = cfg.get("temp_dir")
    create_temp_dir = not os.path.exists(temp_dir)
    if create_temp_dir:
        os.makedirs(temp_dir, exist_ok=True)
    if repo != "all":
        deploy_repo(repo_name=repo)
    else:
        for r in cfg.get("repos", []):
            deploy_repo(repo_name=r["name"])

    os.chdir(start_dir)
    if create_temp_dir and not cfg.get("preserve_temp"):
        os.rmdir(temp_dir)
    print("Deployment complete!")
