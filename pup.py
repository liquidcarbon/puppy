# -*- coding: utf-8 -*-

__doc__ = """
The CLI for pup, a cute python project manager.
"""

__version__ = "2.0.0"

import collections
import json
import platform
import subprocess
import sys
from pathlib import Path
from time import strftime
from typing import Any, Dict, Tuple

import click
import tomllib


class PupException(Exception):
    pass


class Pup:
    """Settings and initialization for pup CLI.

    Puppy is designed to work the same from anywhere within the project folder.
    This means there's some discovery to be done at every invocation,
    so we run Pup.welcome() prior to main().
    """

    COLOR: str = "yellow"
    FILE: Path = Path(__file__)
    HOME: Path = Path(__file__).parent  # initial assumption
    HOME_MARKER: str = "pup.py"
    LOG_FILE: Path = Path("woof.log")
    LOG_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    PLATFORM: str = platform.system()
    PYTHON: Path = Path(sys.executable)
    PYTHON_VER: str = f"{sys.version_info.major}.{sys.version_info.minor}"
    SP_PREFIX: str = "Lib" if PLATFORM == "Windows" else f"lib/python{PYTHON_VER}"
    SP_VENV: str = f".venv/{SP_PREFIX}/site-packages"
    SP_ROOT_PATH: Path = Path(sys.prefix) / SP_PREFIX / "site-packages"
    SP_ROOT_PUP: Path = SP_ROOT_PATH / "pup.py"
    VENV_MARKER: str = "pyproject.toml"

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
        """Pup's origins."""
        return f"🐶 = {cls.PYTHON} {cls.FILE}  # v{__version__}"

    @classmethod
    def welcome(cls) -> None:
        """Prep pup's environment."""
        cls.HOME = cls.find_home()
        cls.SP_ROOT_PUP.write_text(cls.FILE.read_text())
        cls.LOG_FILE = cls.HOME / cls.LOG_FILE
        if not cls.LOG_FILE.exists():
            cls.log(f"🐶 has arrived to {cls.HOME}", cls.LOG_FILE)

    @staticmethod
    def log(
        msg: str, file: Path | None = None, color: str | None = None, tee: bool = True
    ) -> None:
        """Log to stdout.  Tee also logs to file (like '| tee -a $LOG_FILE')."""
        timestamp = strftime(Pup.LOG_TIME_FORMAT)
        log_message = f"[{timestamp}] {msg}"
        click.secho(log_message, fg=color)
        if file and tee:
            with open(file, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")

    @staticmethod
    def do(command: str, tee: bool = True) -> None:
        Pup.say(command, tee=tee)
        subprocess.run(command.split())

    @staticmethod
    def hear(message: str, tee: bool = True) -> None:
        """Log pup's input."""
        Pup.log(f"🐶 heard: {message}", Pup.LOG_FILE, None, tee)

    @staticmethod
    def say(message: str, tee: bool = True) -> None:
        """Log pup's output."""
        Pup.log(f"🐶 said: {message}", Pup.LOG_FILE, Pup.COLOR, tee)

    @staticmethod
    def list_venvs() -> list[Path]:
        """List of virtual environments known to pup.

        A virtual environment is a non-hidden folder that contains
        `Pup.VENV_MARKER` file (`pyproject.toml` by default).
        """

        _venvs = []
        for d in Pup.HOME.iterdir():
            if not d.is_dir() or d.name.startswith("."):
                continue
            _venvs.extend(d.rglob(Pup.VENV_MARKER))

        return [p.parent for p in _venvs if ".venv" not in str(p)]

    @staticmethod
    def load_pyproject(path: Path) -> Dict[str, Any]:
        """Load folder's `pyproject.toml` file."""
        return tomllib.load((path / "pyproject.toml").open("rb"))

    # @staticmethod
    # def verbose(fn: Callable) -> Callable:
    #     click.echo("decorator for CLI commands")
    #     return fn


class Notebook:
    """Templates and env managers for `pup play`."""

    # SITE_PACKAGES_PATH: Path = Path(
    #     r".venv\Lib\site-packages"
    #     if Pup.PLATFORM == "Windows"
    #     else f".venv/bin/python{Pup.PYTHON_VER}/site-packages"
    # ).absolute()

    @staticmethod
    def install_nb_package(engine: str):
        with open(Pup.HOME / "pixi.toml") as f:
            pixi_toml = f.read()
            if engine == "marimo":
                if "marimo" not in pixi_toml:
                    Pup.do("pixi add marimo")
            elif engine == "notebook":
                if "jupyter" not in pixi_toml:
                    Pup.do("pixi add jupyter")
            elif engine == "lab":
                if "jupyterlab" not in pixi_toml:
                    Pup.do("pixi add jupyterlab")
            else:
                Pup.say(f"notebook engine '{engine}' not supported")
                exit(1)
        return


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
    RemoveWhere = click.style("Specify folder/venv from where to remove packages", fg=COLOR)
    RemoveWhat = click.style("Specify what to remove", fg=COLOR)
    FetchWhat = click.style("Choose venv to fetch", fg=COLOR)


class OrderedGroup(click.Group):
    """Class to register commands in the order in which they're written."""

    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


# prep Pup attributes before setting up CLI
Pup.welcome()


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
def uv_init(folder: str, **uv_options: Dict[str, Any]):
    """Create new project and virtual environment with `uv init`."""

    if folder is None:
        folder = click.prompt(UserInput.NewVenvFolder)
    Pup.hear(f"pup new {folder}")

    if folder in ("", "."):
        Pup.say("use `pixi add` to install packages in pup's home folder")
        exit(1)
    if (Pup.HOME / folder).exists():
        if not click.confirm(UserInput.NewVenvFolderOverwrite.format(folder), default="y"):
            return

    Pup.do(f"pixi run uv init {Pup.HOME / folder} -p {Pup.PYTHON} --no-workspace")
    Pup.do(f"pixi run uv venv {Pup.HOME / folder}/.venv -p {Pup.PYTHON}")


@main.command(name="add", context_settings={"ignore_unknown_options": True})
@click.argument("folder", nargs=1, required=False)
@click.argument("packages", nargs=-1, required=False)
def uv_add(folder: str, packages: Tuple[str], **uv_options: Dict[str, Any]):
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

    Pup.do(f"pixi run uv add {packages} --project {folder_abs_path}")


@main.command(name="remove")
@click.argument("folder", nargs=1, required=False)
@click.argument("packages", nargs=-1, required=False)
def uv_remove(folder: str, packages: Tuple[str], **uv_options: Dict[str, Any]):
    """Remove packages from specified venv with `uv remove`."""

    if folder is None:
        folder = click.prompt(UserInput.RemoveWhere)
    if packages in (None, ()):
        packages = click.prompt(UserInput.RemoveWhat).split()
    folder_abs_path = (Pup.HOME / folder).absolute()
    packages = " ".join(packages)
    Pup.hear(f"pup remove {folder} {packages}")

    Pup.do(f"pixi run uv remove {packages} --project {folder_abs_path}")


@main.command(name="list")
@click.argument("venv", required=False)
def pup_list(venv: str | None = None) -> Dict[str, str]:
    """List venvs and their `pyproject.toml` dependencies."""

    Pup.hear(f"pup list {venv}")
    pup_venvs = Pup.list_venvs()
    pup_venvs_dict = {
        str(p.relative_to(Pup.HOME)): Pup.load_pyproject(p)
        .get("project", {})
        .get("dependencies", None)
        for p in pup_venvs
    }
    if venv:
        pup_venvs_dict = {venv: pup_venvs_dict.get(venv, None)}
    click.secho(
        json.dumps(pup_venvs_dict, indent=2),
        fg=Pup.COLOR,
    )


@main.command(name="play")
@click.option(
    "--engine",
    "-e",
    type=click.Choice(["marimo", "notebook", "lab"]),
    default="marimo",
    help="notebook engine",
)
@click.option(
    "--kernel",
    "-k",
    type=click.Choice([p.stem for p in Pup.list_venvs()]),
    help=(
        "pup notebook kernels are folders created by uv "
        "that contain `pyproject.toml` and `.venv/` with installed packages"
    ),
)
def play(engine: str, kernel: str):
    """Create a notebook in a specified environment."""

    Notebook.install_nb_package(engine)


if __name__ == "__main__":
    # CLI
    main()
else:
    # runs on "import pup"
    def fetch(venv: str | None = None, *packages: str) -> None:
        pup_venvs = Pup.list_venvs()
        venvs_names = [str(p.relative_to(Pup.HOME)) for p in pup_venvs]
        Pup.log(f"🐶 virtual envs available: {venvs_names}", file=None, tee=False)
        while not venv:
            venv = click.prompt(UserInput.FetchWhat)
        venv_sp_path = Pup.HOME / venv / Pup.SP_VENV
        if venv_sp_path.exists():
            if len(packages) > 0:
                uv_add.callback(folder=venv, packages=packages)
            sys.path.append(str(venv_sp_path))
            pup_list.callback(venv)
            Pup.log(
                f"fetched packages from '{venv}': {venv_sp_path} added to `sys.path`",
                file=None,
                tee=False,
            )
        else:
            uv_add.callback(folder=venv, packages=packages)
            fetch(venv)
        return
