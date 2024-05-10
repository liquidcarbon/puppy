#!/home/a/Desktop/puppy/.pixi/envs/default/bin/python
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
PUP_UV = PUP_PIXI_ENV / ("Library/bin/uv.exe" if PLATFORM == "Windows" else "bin/uv")
VENV_PYTHON_SUBPATH = "Scripts/python.exe" if PLATFORM == "Windows" else "bin/python"


def log(message, file=PUP_LOG):
    """Log to file."""
    timestamp = datetime.now().strftime(PUP_LOG_TIME_FORMAT)
    log_message = f"[{timestamp}] {message} "
    if file != "-":
        with open(file, "a", encoding='utf-8') as f:
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
    NEW_VENV_FOLDER = click.style("Folder to create venv in", fg="bright_cyan")
    NEW_VENV_OVERWRITE = click.style("Folder `{}` already exists. Overwrite?", fg="red")


@click.group()
def main():
    """Call pup and friends for all your python needs."""
    pass

@main.command(name="fetch")
@click.argument('where', nargs=1, required=False)
@click.argument('what', nargs=-1, required=False)
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

@main.command(name="new")
@click.argument('where', nargs=1, required=False)
def new_venv(where):
    """Create a new virtual environment in <WHERE> folder."""
    if where is None:
        where = click.prompt(UserInput.NEW_VENV_FOLDER)
    if where == ".":
        tee("use pixi to isntall packages in pup's home folder")
        return
    if (PUP_HOME / where).exists():
        if not click.confirm(UserInput.NEW_VENV_OVERWRITE.format(where)):
            return
    log(f"pup new {where}")
    cmd = f"{PUP_UV} venv {PUP_HOME / where}/.venv"
    tee(cmd)
    subprocess.run(cmd, shell=True)


@main.command()
def which():
    """Show 🐶's current home."""
    log("pup which")
    tee(f"home is {PUP_HOME}")
    # tee(f"home is {PUP_HOME}", file="-")  # stdout only


if __name__ == '__main__':
    main()
