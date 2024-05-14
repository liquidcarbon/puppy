# -*- coding: utf-8 -*-
__doc__ = """
🐶 Puppy 0.2.1
---------------
Tested with:
✨ Pixi 0.22.0
🎆 uv 0.1.43
"""


import click
import platform
import subprocess
import tomllib
from datetime import datetime
from pathlib import Path

PLATFORM = platform.system()
PUP_COLOR = "yellow"
PUP_FILE = Path(__file__).absolute()
PUP_HOME = Path(__file__).parent
PUP_LOG = PUP_HOME / "woof.log"
PUP_LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PUP_PIXI_ENV = PUP_HOME / ".pixi/envs/default"
PUP_PYTHON = PUP_PIXI_ENV  / ("python.exe" if PLATFORM == "Windows" else "bin/python")
PUP_UV = PUP_PIXI_ENV / ("Library/bin/uv.exe" if PLATFORM == "Windows" else "bin/uv")
VENV_PYTHON_SUBPATH = "Scripts/python.exe" if PLATFORM == "Windows" else "bin/python"


def log(message, file=PUP_LOG):
    """Log to file."""
    timestamp = datetime.now().strftime(PUP_LOG_TIME_FORMAT)
    log_message = f"[{timestamp}] {message} "
    if file != "-":
        with open(file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    return log_message

def tee(message, file=PUP_LOG):
    """Emit message to console and log to file (like '| tee -a $PUP_LOG')."""
    log_message = log(f"🐶 says: {message}", file)
    click.secho(log_message, fg=PUP_COLOR)


### CLI ###

class UserInput:
    FETCH_NEW_VENV = click.style(
        "Environment `{}` does not exist. Create it?",
        fg="bright_cyan")
    FETCH_WHAT = click.style("Specify what to install", fg="bright_cyan")
    FETCH_WHERE = click.style(
        "Specify folder/environment where to fetch packages",
        fg="bright_cyan"
    )
    NEW_KERNEL = click.style("Create kernel for which venv", fg="bright_cyan")
    NEW_KERNEL_NAME = click.style(
        "Name of the kernel (allowed characters: [a-zA-Z0-9.-_])",
        fg="bright_cyan"
    )
    NEW_VENV_FOLDER = click.style("Folder to create venv in", fg="bright_cyan")
    NEW_VENV_KERNEL = click.style(
        "Would you like to create a new Jupyter kernel",
        fg="bright_cyan"
    )
    NEW_VENV_OVERWRITE = click.style("Folder `{}` already exists. Overwrite?", fg="red")


@click.group()
def main():
    """Call pup and friends for all your python needs."""
    pass

@main.command(name="fetch", context_settings={"ignore_unknown_options": True})
@click.argument("where", nargs=1, required=False)
@click.argument("what", nargs=-1, required=False)
def uv_install(where, what):
    """Fetch (install) packages with uv."""
    if where is None:
        where = click.prompt(UserInput.FETCH_WHERE)
    if what in (None, ()):
        what = click.prompt(UserInput.FETCH_WHAT).split()
    what = " ".join(what)
    log(f"pup fetch {where} {what}")
    
    py_path = PUP_HOME / where / ".venv" / VENV_PYTHON_SUBPATH
    if not (PUP_HOME / where).exists() or not py_path.exists():
        if click.confirm(UserInput.FETCH_NEW_VENV.format(where)):
            new_venv.callback(where=where)
        else:
            return
    
    cmd = f"""{PUP_UV} pip install {what} -p {py_path}"""
    tee(cmd)
    subprocess.run(cmd.split())

@main.command(name="kernel")
@click.argument("where", nargs=1, required=False)
@click.argument("kernel_name", nargs=1, required=False)
def new_kernel(where, kernel_name):
    """Interactively create new ipython kernel linked to 🐶's environment."""
    if where is None:
        where = click.prompt(UserInput.NEW_KERNEL)
    uv_install.callback(where=where, what=("ipykernel",))
    if kernel_name is None:
        kernel_name = click.prompt(
            UserInput.NEW_KERNEL_NAME,
            default=f"{where}-{get_python_major_minor()}"
        )
    
    py_path = PUP_HOME / where / ".venv" / VENV_PYTHON_SUBPATH
    log(f"pup kernel {where} {kernel_name}")
    cmd = f"{py_path} -m ipykernel install --name {kernel_name} --prefix {PUP_PIXI_ENV}"
    tee(cmd)
    subprocess.run(cmd)


@main.command(name="list")
@click.argument("where", nargs=1, required=True)
def list_packages(where):
    """List packages."""
    if where == ".":
        cmd="pixi run uv pip list"
    else:
        py_path = PUP_HOME / where / ".venv" / VENV_PYTHON_SUBPATH
        cmd = f"""{PUP_UV} pip list -p {py_path}"""
    tee(cmd)
    subprocess.run(cmd)


@main.command(name="new")
@click.argument("where", nargs=1, required=False)
def new_venv(where):
    """Create a new virtual environment in <WHERE> folder."""
    if where is None:
        where = click.prompt(UserInput.NEW_VENV_FOLDER)
    if where == ".":
        tee("use pixi to install packages in pup's home folder")
        exit(1)
    if (PUP_HOME / where).exists():
        if not click.confirm(UserInput.NEW_VENV_OVERWRITE.format(where)):
            return
    log(f"pup new {where}")
    cmd = f"{PUP_UV} venv {PUP_HOME / where}/.venv -p {PUP_PYTHON}"
    tee(cmd)
    subprocess.run(cmd)
    if click.confirm(UserInput.NEW_VENV_KERNEL):
        new_kernel.callback(where=where, kernel_name=None)


@main.command()
def which():
    """Show 🐶's current home."""
    log("pup which")
    tee(f"home is {PUP_HOME}")
    # tee(f"home is {PUP_HOME}", file="-")  # stdout only


### Utils ###

def get_python_major_minor():
    return ".".join(platform.python_version_tuple()[:2])


### Entry Point ###

if __name__ == '__main__':
    main()
