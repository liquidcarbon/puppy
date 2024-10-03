import sys

import typer


class Pup:
    FILE: str = __file__
    LOG_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    PYTHON: str = sys.executable

    @classmethod
    def pedigree(cls):
        return f"pedigree: {cls.PYTHON} {cls.FILE}"


app = typer.Typer(no_args_is_help=True, add_completion=False, help=Pup.pedigree())


@app.command()
def new(where: str):
    """Create new environment."""
    cmd = f"{where} "
    # tee(cmd)
    typer.echo(cmd)


@app.command()
def hi():
    """Say hi to pup"""
    typer.echo("🐶 says: woof!")


if __name__ == "__main__":
    app()
