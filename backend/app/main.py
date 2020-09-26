import click
import uvicorn
from app.core.factory import create_app
from app.core.upload_worker.factory import create_worker


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("--reload", is_flag=True)
def run(reload: bool = False) -> None:
    if reload:
        uvicorn.run("app.importable_app:app", host="0.0.0.0", port=8000, reload=True)
    else:
        app = create_app()
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)


@cli.command()
def worker() -> None:
    create_worker()


if __name__ == "__main__":
    cli()
