import typer

from tfds.commands import cfg, dc, nb

app = typer.Typer()

app.command()(dc.dc)
app.add_typer(nb.nb_app, name="nb")
app.add_typer(cfg.cfg_app, name="cfg")

if __name__ == "__main__":
    app()
