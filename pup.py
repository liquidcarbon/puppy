# -*- coding: utf-8 -*-
__doc__ = """
The CLI for pup, a cute python package manager.
"""

import click
import json
import platform
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from time import sleep, strftime, time

PLATFORM = platform.system()
PUP_COLOR = "yellow"
PUP_FILE = Path(__file__).absolute()
PUP_HOME = Path(__file__).parent
PUP_LOG = PUP_HOME / "woof.log"
PUP_LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PUP_NOTEBOOKS = PUP_HOME / "notebooks"
PUP_PIXI_ENV = PUP_HOME / ".pixi/envs/default"
PUP_PYTHON = PUP_PIXI_ENV  / ("python.exe" if PLATFORM == "Windows" else "bin/python")
PUP_UV = PUP_PIXI_ENV / ("Library/bin/uv.exe" if PLATFORM == "Windows" else "bin/uv")
VENV_PYTHON_SUBPATH = "Scripts/python.exe" if PLATFORM == "Windows" else "bin/python"


def log(message, file=PUP_LOG):
    """Log to file."""
    timestamp = strftime(PUP_LOG_TIME_FORMAT)
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
    DROP_WHAT = click.style("Specify which packages to drop (uninstall)", fg="bright_cyan")
    DROP_FROM_WHERE = click.style(
        "Specify folder/environment from which to remove packages",
        fg="bright_cyan"
    )
    FETCH_NEW_VENV = click.style(
        "Environment `{}` does not exist. Create it?",
        fg="bright_cyan"
    )
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
    PLAY_OVERWRITE = click.style("File `{}` exists. Overwrite?", fg="bright_cyan")


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
        if confirm(UserInput.FETCH_NEW_VENV.format(where), default=True):
            new_venv.callback(where=where)
        else:
            return
    
    cmd = f"""{PUP_UV} pip install {what} -p {py_path}"""
    tee(cmd)
    subprocess.run(cmd.split())


@main.command(name="drop", context_settings={"ignore_unknown_options": True})
@click.argument("where", nargs=1, required=False)
@click.argument("what", nargs=-1, required=False)
def uv_uninstall(where, what):
    """Drop (remove, uninstall) packages with uv."""
    if where is None:
        where = click.prompt(UserInput.DROP_FROM_WHERE)
    if what in (None, ()):
        what = click.prompt(UserInput.DROP_WHAT).split()
    what = " ".join(what)
    log(f"pup drop {where} {what}")
    
    py_path = PUP_HOME / where / ".venv" / VENV_PYTHON_SUBPATH
    cmd = f"""{PUP_UV} pip uninstall {what} -p {py_path}"""
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
    subprocess.run(cmd.split())


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
    subprocess.run(cmd.split())


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
        if not confirm(UserInput.NEW_VENV_OVERWRITE.format(where), default="y"):
            return
    log(f"pup new {where}")
    cmd = f"{PUP_UV} venv {PUP_HOME / where}/.venv -p {PUP_PYTHON}"
    tee(cmd)
    subprocess.run(cmd.split())


@main.command(name="play")
@click.option(
    "--jupyter", "-j",
    type=click.Choice(["notebook", "lab"]),
    default="notebook",
    help="jupyter flavor"
)
@click.option("--ip", "-i", default="0.0.0.0", help="Jupyter Server IP (default: 0.0.0.0)")
@click.option("--port", "-p", default="8880", help="Jupyter Server port (default: 8880)")
@click.option("--nb-dir", "-d", default=PUP_HOME, help="Starting Notebook Dir")
@click.option("--name", "-n", default=None, help="notebook name (default: timestamp)")
@click.option("--kernel-name", "-k", default="python3", help="kernel name")
# @click.option("--modify", "-M", is_flag=True, default=False, help="modify existing notebook (no_prompt)")
@click.option(
    "--ex/--no-ex", "-E/-X",
    default=False,
    help="execute notebook (default: no)"
)
@click.option(
    "--start/--no-start", "-S/-N",
    default=True,
    help="start jupyter (default: start)"
)
@click.option(
    "--code", "-c", multiple=True,
    help="""\b
        add code or markdown cells
        use `;` (no spaces) to separate code lines
        prefix markdown cells with `md|`
        ------------------------------------------------
        with -n option and -c blocks, pup will write new
        or ask to overwrite an existing notebook;
        with -n option but no -c blocks, pup will try to
        open or execute an existing notebook;
        without -n, pup will create a new notebook named
        `<epoch time>.ipynb` with some starter code.
        ------------------------------------------------
    """
)
def do_jupyter(jupyter, ip, port, nb_dir, name, kernel_name, ex, start, code):
    """Generate, execute, or open jupyter notebook with added code cells."""

    PUP_NOTEBOOKS.mkdir(exist_ok=True)
    nb_file = PUP_NOTEBOOKS / (name or f"{int(time())}.ipynb")
    
    if not nb_file.exists():
        # inject some starter code if none provided
        code = code or (
                "md|# Title",
                "import sys;py = sys.executable;print(py);"
                "!pixi run uv pip list -p $py",
                """print("notebook run complete")"""
            )

    if code:
        overwrite_prompt = UserInput.PLAY_OVERWRITE.format(nb_file)
        if not nb_file.exists() or confirm(overwrite_prompt):
            IPYNB.create(nb_file, kernel_name, ex, *code)
            tee(f"{nb_file} created")
    else:
        pass  # file exists, no code provided: open file
  
    if ex:
        tee(f"executing notebook {nb_file} using {kernel_name}...")
        IPYNB.run_nbclient(nb_file, kernel_name)
        tee(f"done")

    if start:
        cmd = f"""pixi run jupyter {jupyter} {nb_file} --notebook-dir="{nb_dir}"  --ip={ip} --port={port}"""
        tee(cmd)
        subprocess.run(cmd.split())


@main.command()
def which():
    """Show 🐶's current home."""
    log("pup which")
    tee(f"home is {PUP_HOME}")
    # tee(f"home is {PUP_HOME}", file="-")  # stdout only


### Utils ###

def confirm(text, **kwargs) -> bool:
    """Prompt with click.confirm or silently return True in non-interactive shells."""
    if sys.stdin.isatty() or hasattr(sys, "ps1"):
        return click.confirm(text, **kwargs)
    else:
        return True

def get_python_major_minor():
    return ".".join(platform.python_version_tuple()[:2])


### Templates ###

class IPYNB:
    """Templates and methods for populating IPython notebooks from CLI."""

    TEMPLATE = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "name": None
            },
            "language_info": {
                "name": ""
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    CELL = {
        "cell_type": None,
        "metadata": {},
        "source": [],
    }
    
    def parse_cell(source: str) -> dict:
        """Parse CLI `--code` option into an IPYNB cell dict"""
        ipynb_cell = deepcopy(IPYNB.CELL)
        if len(source) > 2 and source[:3] == "md|":
            source = source[3:]
            cell_type = "markdown"
        else:
            cell_type = "code"
            ipynb_cell["execution_count"] = None
            ipynb_cell["outputs"] = []
        lines = [line+"\n" for line in source.split(";")]
        lines[-1] = lines[-1][:-1]
        ipynb_cell["source"] = lines
        ipynb_cell["cell_type"] = cell_type
        ipynb_cell["id"] = str(time())[-4:]; sleep(1e-4)  # pseudorandom
        return ipynb_cell

    def create(nb_file: Path, kernel_name: str, ex: bool, *code) -> Path:
        """Create notebook dict, return path to notebook."""

        nb_file.parent.mkdir(exist_ok=True)
        ipynb = deepcopy(IPYNB.TEMPLATE)
        ipynb.update(
            **{"cells": [IPYNB.parse_cell(cell) for cell in code]}
        )
        ipynb["metadata"]["kernelspec"]["name"] = kernel_name
        ipynb["metadata"]["kernelspec"]["display_name"] = kernel_name
        with open(nb_file, "w") as f:
            json.dump(ipynb, f)
        
    def run_nbclient(nb_file: Path, kernel_name: str):
        """Execute notebook with nbclient."""
        import nbformat
        from nbclient import NotebookClient
        nb = nbformat.read(nb_file, as_version=4)
        client = NotebookClient(
            nb, kernel_name=kernel_name,
            timeout=120, allow_errors=True, log_level=40
        )
        client.execute(cwd=nb_file.parent)
        nbformat.write(nb, nb_file)


### Entry Point ###

if __name__ == '__main__':
    main()
