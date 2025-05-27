import typer

from tfds_cli.commands import dc, nb, stack

app = typer.Typer()

app.command()(dc.dc)
app.add_typer(nb.nb_app, name="nb")
app.add_typer(stack.cfg_app, name="stack")

if __name__ == "__main__":
    app()
