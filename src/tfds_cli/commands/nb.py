import typer

nb_app = typer.Typer()


@nb_app.command()  # type: ignore
def deploy(nb: str = typer.Option(..., "--nb", help="Notebook name")) -> None:
    """Deploy all notebooks to S3, timestamping and tagging them with git revision."""
    typer.echo(f"Deploy notebook: {nb}")


@nb_app.command()  # type: ignore
def ls() -> None:
    """List all notebooks on S3."""
    typer.echo("List notebooks")


@nb_app.command()  # type: ignore
def deletes3(nb: str = typer.Option(..., "--nb", help="Notebook name")) -> None:
    """Delete all or a single notebook on s3."""
    typer.echo(f"Clear notebook: {nb}")
