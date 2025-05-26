from typing import List

import typer


def dc(
    service: str = typer.Option("current-stack", "--service", "-s", help="Service name"),
    extra: List[str] = typer.Argument(..., help="Docker compose parameters"),
) -> None:
    """
    Call docker compose for all tfds plugins in the current stack or for a single plugin.

    """
    typer.echo(f"dc called with service={service}")
    typer.echo(f"Extra params: {extra}")
