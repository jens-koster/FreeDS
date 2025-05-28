import os
import subprocess
from pathlib import Path
from typing import List, Optional, cast

from tfdslib.config import get_config

from tfds_cli.utils.stackutils import (
    get_current_stack,
    get_stack_config,
    get_stack_names,
)


def set_secret_envs() -> None:
    """Set our secrets in environment variables; TFDS_<PLUGIN>_<KEY>."""
    config_cfg = get_config("config")
    os.environ["TFDS_CONFIG_URL"] = config_cfg.get("url", "http://tfds-config:8005/api/configs")
    secrets = ["minio", "s3"]  # todo: make this a config...
    for secret in secrets:
        config = get_config(secret)
        for key, value in config.items():
            if isinstance(value, str) and value.startswith("~/"):
                value = str(Path(value).expanduser())
            if isinstance(value, list):
                value = ",".join(map(str, value))
            env_var = f"TFDS_{secret}_{key}".upper()
            os.environ[env_var] = str(value)


def get_plugins(single: str = "current-stack") -> Optional[List[str]]:
    current_stack = get_current_stack()
    if current_stack is None:
        print("Error: No current stack set. Use `tfds setstack <stackname>` to set a stack.")
        return None

    cfg = get_stack_config(current_stack)
    if not cfg:
        print(f"Current stack {current_stack} is not defined in stacks config, available stacks: {get_stack_names()}")
        return None

    plugins = cfg.get("plugins")
    if not plugins:
        print(f'Error: malformed config, "plugins" key is missing on stack{current_stack}.')
        return None

    if single and single != "current-stack":
        if single in plugins:
            print(f"Single plugin specified: {single}")
            plugins = [single]
        else:
            print(f"Error: plugin '{single}' not found in stack {current_stack}.")
            return None
    return cast(List[str], plugins)


def execute_docker_compose(params: List[str], plugins: List[str]) -> None:
    command = params[0]
    if command in ["down", "stop"]:
        plugins = list(reversed(plugins))
    if command in ["up", "start"] and "-d" not in params:
        params.append("-d")

    dc = ["docker", "compose", *params]

    # Execute the command for each plugin
    start_dir = Path.cwd()
    print(f"Running '{' '.join(dc)}' for plugins: {plugins}")
    set_secret_envs()
    for plugin in plugins:
        plugin_dir = start_dir / plugin
        if not plugin_dir.exists():
            print(f"Warning: Plugin directory '{plugin_dir}' does not exist. Skipping.")
            continue
        os.chdir(plugin_dir)
        try:
            print(f"Executing in: {Path.cwd()}")
            subprocess.run(dc, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to execute 'docker compose {command}' for plugin '{plugin}':{e}.")
        finally:
            os.chdir(start_dir)
