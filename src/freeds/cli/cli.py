import typer

from freeds.cli.commands import dc, nb, selfcheck, stack
from freeds.config import set_env

set_env()


app = typer.Typer()

app.command()(dc.dc)
app.command()(selfcheck.selfcheck)
app.add_typer(nb.nb_app, name="nb")
app.add_typer(stack.cfg_app, name="stack")


if __name__ == "__main__":
    app()
