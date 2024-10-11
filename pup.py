# -*- coding: utf-8 -*-

__doc__ = """
The CLI for pup, a cute python project manager.
"""

__version__ = "2.0.0"

import collections
import platform
import subprocess
import sys
from pathlib import Path
from time import strftime
from typing import Tuple

import click


class PupException(Exception):
    pass


class Pup:
    """Settings and initialization for pup CLI.

    Puppy is designed to work the same from anywhere within the project folder.
    This means there's some discovery to be done at every invokation,
    so we run Pup.welcome() prior to main().
    """

    COLOR: str = "yellow"
    FILE: Path = Path(__file__)
    HOME: Path = Path(__file__).parent  # initial assumption
    HOME_MARKER: str = "pup.py"
    LOG_FILE: Path = Path("woof.log")
    LOG_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    PLATFORM = platform.system()
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
        """Search in current folder and its parents for HOME_MARKER file."""
        if (prefix / cls.HOME_MARKER).exists():
            return prefix
        elif prefix.parent in (prefix, prefix.root):
            # should never happen using Bash/PS runners, only if pup.py used directly
            if click.confirm(UserInput.PupHomeNotFound):
                exit(1)
            else:
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
        if not cls.LOG_FILE.exists():
            cls.log(f"🐶 has arrived to {cls.HOME}", cls.LOG_FILE)

    # @staticmethod
    # def verbose(fn: Callable) -> Callable:
    #     click.echo("decorator for CLI commands")
    #     return fn


class UserInput:
    """User input prompts and other messages."""

    COLOR = "bright_cyan"
    COLOR_WARN = "magenta"
    PupHomeNotFound = click.style(
        f"🐶's {Pup.HOME_MARKER} not found in this folder or its parents;"
        "\nwould you like to set up a new pup home here?",
        fg=COLOR,
    )
    NewVenvFolder = click.style("Folder to create venv in", fg=COLOR)
    NewVenvFolderOverwrite = click.style(
        "Folder `{}` already exists. Overwrite the venv?", fg=COLOR_WARN
    )
    AddWhere = click.style("Specify folder/venv where to add packages", fg=COLOR)
    AddWhat = click.style("Specify what to install", fg=COLOR)


class OrderedGroup(click.Group):
    """Class to register commands in the order in which they're written."""

    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup)
@click.pass_context
def main(ctx):
    """Call pup and friends for all your python needs."""
    pass


@main.command(name="hi")
def say_hi():
    """Say hi to pup."""
    Pup.log(Pup.pedigree(), Pup.LOG_FILE)
    Pup.log(f"🏠 = {Pup.HOME}", Pup.LOG_FILE)
    Pup.log(f"🐍 = {sys.version}", Pup.LOG_FILE)
    Pup.hear("pup hi")
    Pup.say("woof! Nice to meet you. Check woof.log for pup command history")


@main.command(name="new", context_settings={"ignore_unknown_options": True})
@click.argument("folder", nargs=1, required=False)
@click.argument("uv_options", nargs=-1, required=False)
def uv_init(folder: str, **uv_options):
    """Create new project and virtual environment in FOLDER with `uv init`."""

    Pup.hear(f"pup new {folder}")
    if folder is None:
        folder = click.prompt(UserInput.NewVenvFolder)
    if folder in ("", "."):
        Pup.say("use `pixi add` to install packages in pup's home folder")
        exit(1)
    if (Pup.HOME / folder).exists():
        if not click.confirm(UserInput.NewVenvFolderOverwrite.format(folder), default="y"):
            return
    cmd_init = f"pixi run uv init {Pup.HOME / folder} -p {Pup.PYTHON} --no-workspace"
    Pup.say(cmd_init)
    subprocess.run(cmd_init.split())
    cmd_venv = f"pixi run uv venv {Pup.HOME / folder}/.venv -p {Pup.PYTHON}"
    Pup.say(cmd_venv)
    subprocess.run(cmd_venv.split())


@main.command(name="add", context_settings={"ignore_unknown_options": True})
@click.argument("folder", nargs=1, required=False)
@click.argument("packages", nargs=-1, required=False)
def uv_add(folder: str, packages: Tuple[str]):
    """Install packages into specified venv with `uv add`."""
    if folder is None:
        folder = click.prompt(UserInput.AddWhere)
    folder_abs_path = (Pup.HOME / folder).absolute()
    if not folder_abs_path.exists():
        uv_init.callback(folder)
    if packages in (None, ()):
        packages = click.prompt(UserInput.AddWhat).split()
    packages = " ".join(packages)
    Pup.hear(f"pup add {folder} {packages}")
    cmd_add = f"pixi run uv add {packages} --project {folder_abs_path}"
    Pup.say(cmd_add)
    subprocess.run(cmd_add.split())


if __name__ == "__main__":
    Pup.welcome()
    main()
