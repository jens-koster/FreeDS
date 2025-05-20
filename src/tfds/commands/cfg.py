import typer

cfg_app = typer.Typer()
cfg_ls_app = typer.Typer()

cfg_app.add_typer(cfg_ls_app, name="ls")


@cfg_ls_app.command()  # type: ignore
def ls(verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")) -> None:
    if verbose:
        typer.echo("Config ls verbose")
    else:
        typer.echo("Config ls")
