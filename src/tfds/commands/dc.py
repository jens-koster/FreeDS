from typing import List

import typer


def dc(
    service: str = typer.Option(..., "--service", "-s", help="Service name"),
    extra: List[str] = typer.Argument(..., help="Docker compose parameters"),
) -> None:
    """
    Command dc with service and additional arbitrary params.
    """
    typer.echo(f"dc called with service={service}")
    typer.echo(f"Extra params: {extra}")
