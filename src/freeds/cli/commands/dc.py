from typing import List

import typer

from freeds.cli.helpers import execute_docker_compose, get_plugins


def dc(
    single: str = typer.Option(None, "--single", "-s", help="Run for a single plugin"),
    extra: List[str] = typer.Argument(..., help="Docker compose parameters"),
) -> int:
    """
    Call docker compose with the supplied parameters for all freeds plugins in the current stack.
    """

    print(f"Running docker compose for {'all plugins' if single == 'current-stack' else single} in current stack.")

    if not extra:
        print("Error: docker compose command must be given")
        return 1

    plugins: list[str] = []
    if single is None:
        plugins = get_plugins()
        print(f"Found plugins: {plugins}")
    else:
        plugins = [single]

    execute_docker_compose(params=extra, plugins=plugins)
    return 0
