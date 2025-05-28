#!/usr/bin/env python3
from typing import Any, Optional, Union, cast

from tfdslib.config import get_config, set_config


def get_current_stack() -> Union[None, str]:
    """Get the current stack name from the currentstack.yaml file."""
    cur_stack = get_config("currentstack")
    if not cur_stack:
        return None
    stack = cur_stack.get("current_stack")
    return None if stack is None else str(stack)


def get_stack_names() -> list[str]:
    """Get a list of stacknames"""
    stacks = get_config("stacks")
    return list(stacks.keys())


def get_stack_config(stack_name: str) -> Optional[dict[str, Any]]:
    cfg = get_config("stacks")
    return cast(dict[str, Any], cfg.get(stack_name))


def set_current_stack(stack_name: str) -> None:
    """Set tfds to use the provided stack."""
    stack_found = False
    for name in get_stack_names():
        if stack_name == name:
            stack_found = True
            break
    if not stack_found:
        print(f"Error: Stack '{stack_name}' not found, use `tfds ls` to see available stacks.")

    # Lock the file to prevent race conditions
    config = {
        "annotation": "the current stack for tfds cli, use setstack to change it, editing here is fine too",
        "config": {"current_stack": stack_name},
    }
    set_config("currentstack", config)
    print(f"Current stack set to '{stack_name}'.")
