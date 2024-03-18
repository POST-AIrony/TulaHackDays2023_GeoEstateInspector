import os

import typer
import uvicorn
from core import settings

cli = typer.Typer()


@cli.command()
def run():
    if __name__ == "__main__":
        uvicorn.run("core.app:app", host=settings.HOST, port=settings.PORT)


@cli.command()
def tdq():
    os.system("dramatiq core.tdq")


if __name__ == "__main__":
    cli()
