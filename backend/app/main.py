import os

import click
import uvicorn
from app.core.factory import create_app


@click.group()
def cli():
    pass


@cli.command()
@click.option("--reload", is_flag=True)
def run(reload=False):
    if reload:
        uvicorn.run("app.importable_app:app", host="0.0.0.0", port=8000, reload=True)
    else:
        app = create_app()
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    cli()
