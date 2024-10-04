# -*- coding: utf-8 -*-
__doc__ = """
The CLI for pup, a cute python project manager.
"""

import sys
from pathlib import Path

import click


class PupException(Exception):
    pass


class Pup:
    FILE: Path = Path(__file__)
    LOG_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    PUP_HOME_MARKER: str = "woof.log"
    PYTHON: Path = Path(sys.executable)
    PYTHON_PREFIX: Path = Path(sys.prefix)

    @classmethod
    def find_home(cls, prefix=PYTHON_PREFIX) -> Path:
        if (prefix / cls.PUP_HOME_MARKER).exists():
            return prefix
        elif prefix.parent == prefix:
            _home = cls.PUP_HOME_MARKER
            click.echo(f"🐶's {_home} not found in this folder or its parents")
            exit(1)
        else:
            return cls.find_home(prefix.parent)

    @classmethod
    def pedigree(cls) -> str:
        return f"🐶 = {cls.PYTHON} {cls.FILE}"


@click.group
@click.pass_context
def main(ctx):
    """Call pup and friends for all your python needs."""
    pass


@main.command(name="hi")
def say_hi():
    """Say hi to pup."""
    click.echo(Pup.pedigree())
    click.echo(f"🐶 home is: {Pup.find_home()}")
    click.echo("🐶 says: woof! check woof.log for pup command history")


if __name__ == "__main__":
    main()
