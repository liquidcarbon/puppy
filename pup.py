# -*- coding: utf-8 -*-
__doc__ = """
The CLI for pup, a cute python project manager.
"""

import sys
from pathlib import Path
from time import strftime

import click


class PupException(Exception):
    pass


class Pup:
    """Settings and initialization for pup CLI.

    Puppy is designed to work from anywhere inside project folder.
    This means there's some discovery to be done at every invokation,
    so we run Pup.welcome() prior to main().
    """

    COLOR: str = "yellow"
    FILE: Path = Path(__file__)
    HOME_MARKER: Path = Path("woof.log")
    LOG_FILE: Path = Path("woof.log")
    LOG_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    PYTHON: Path = Path(sys.executable)

    @staticmethod
    def log(message: str, file: Path, fg_color: str | None = None, tee: bool = True):
        """Log to stdout.  Tee also logs to file (like '| tee -a $LOG_FILE')."""
        timestamp = strftime(Pup.LOG_TIME_FORMAT)
        log_message = f"[{timestamp}] {message}"
        click.secho(log_message, fg=fg_color)
        if tee:
            with open(file, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")

    @staticmethod
    def hear(message: str, tee: bool = True):
        """Log pup's input."""
        Pup.log(f"🐶 heard: {message}", Pup.LOG_FILE, None, tee)

    @staticmethod
    def say(message: str, tee: bool = True):
        """Log pup's output."""
        Pup.log(f"🐶 said: {message}", Pup.LOG_FILE, Pup.COLOR, tee)

    @classmethod
    def find_home(cls, prefix: Path = Path(sys.prefix)) -> Path:
        if (prefix / cls.HOME_MARKER).exists():
            return prefix
        elif prefix.parent == prefix:
            _home = cls.HOME_MARKER
            click.echo(f"🐶's {_home} not found in this folder or its parents")
            exit(1)
        else:
            return cls.find_home(prefix.parent)

    @classmethod
    def pedigree(cls) -> str:
        return f"🐶 = {cls.PYTHON} {cls.FILE}"

    @classmethod
    def welcome(cls):
        """Prep pup's environment."""
        cls.HOME = cls.find_home()
        cls.LOG_FILE = cls.HOME / cls.LOG_FILE
        if cls.LOG_FILE.stat().st_size == 0:
            cls.log(f"🐶 has arrived to {cls.HOME}", cls.LOG_FILE)
            cls.say("woof!")

    # @staticmethod
    # def verbose(fn: Callable) -> Callable:
    #     click.echo("decorator for CLI commands")
    #     return fn


@click.group
@click.pass_context
def main(ctx):
    """Call pup and friends for all your python needs."""
    pass


@main.command(name="hi")
def say_hi():
    """Say hi to pup."""
    click.echo(Pup.pedigree())
    click.echo(f"🏠 = {Pup.HOME}")
    click.echo(f"🐍 = {sys.version}")
    Pup.say("woof! Nice to meet you. Check woof.log for pup command history", tee=0)


if __name__ == "__main__":
    Pup.welcome()
    main()
