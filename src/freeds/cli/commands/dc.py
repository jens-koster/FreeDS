from typing import List

import typer

from freeds.utils import execute_docker_compose, get_plugins


def dc(
    single: str = typer.Option("current-stack", "--single", "-s", help="Run for a single plugin"),
    extra: List[str] = typer.Argument(..., help="Docker compose parameters"),
) -> int:
    """
    Call docker compose with the supplied parameters for all tfds plugins in the current stack.
    """

    print(f"Running docker compose for {'all plugins' if single == 'current-stack' else single} in current stack.")

    if not extra:
        print("Error: docker compose command must be given")
        return 1

    plugins = get_plugins(single)
    if plugins is None:
        print(f"Error: could not retrieve plugins for stack '{single}'.")
        return 1
    else:
        print(f"Found plugins: {plugins}")

    execute_docker_compose(params=extra, plugins=plugins)
    return 0
