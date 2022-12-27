from sparrow_cli.api import app
from sparrow_cli.consoles import console
from sparrow_cli import __version__


@app.command()
def version():
    """CLI's version"""
    console.print(f"Sparrow CLI {__version__}")
