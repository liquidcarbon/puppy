# This is the installation Bash script for Puppy.

# IMPORTANT: pup will never touch or modify your system python.
# Except for Pixi, nothing is permanently placed on PATH.
# The base python installation and all virtual environments will
# reside in one folder, the one from which you call this script.

# From a folder that will become your pup/python home, call:

# curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh

# This script checks for the tools that pup requires and installs or updates them.
# It will ask for the desired python version and use the latest versions of the other tools.

# 1) pup.py
# 2) pixi (see https://pixi.sh to learn more about Pixi)
# 3) base python (strictly one per pup/py home)
# 4) uv (see https://github.com/astral-sh/uv to learn more about uv)
# 5) click (see https://github.com/pallets/click to learn more about click)

# In the final step, the script can export an alias "pup" pointed to "./pup.py".
# This alias is not permanent, by design, to easily between different base pup/pythons.
# Whenever you open a new terminal, simply call the last line of this script again to
# recreate the alias.  Running this script from another folder will setup/activate another
# pup/python base.  If another base python is needed, simply run this script again
# from another folder.
# Do not nest pup/py folders.

# A pup/py home is defined by one and only one python executable, which is managed by pixi,
# along with tools like uv, jupyter, hatch, pytest, and conda-managed packages.
# We use home-specific tools through a pixi shell from anywhere within the folder,
# e.g. `pixi run python`, `pixi run jupyter`, or by calling their absolute paths.

# The blueprint for a pup/py home is in `pixi.toml`; at this level, git is not needed.
# The inner folders are git-ready project environments managed by pup and uv.
# In each of the inner folders, there is a classic `.venv` folder populated by uv, and
# a `pyproject.toml` file that is kept in sync with the environment by pup.

# ├── puphome
# │   ├── env1
# │   │   ├── .venv
# │   │   └── pyproject.toml
# │   ├── env2
# │   │   ├── .venv
# │   │   └── pyproject.toml
# │   ├── pixi.toml
# │   └── pup.py
# ├── pup311torch
# │   ├── env3
# │   └── env4
# └── pup313beta
#     └── env5

# ────────────────────────────
# Illustration of pup/py homes


DEFAULT_PY_VERSION="3.12"
PIXI_INSTALL_URL="https://pixi.sh/install.sh"
PIXI_PUP_HOME="$(pwd)"  # initial assumption; will check parent paths
PUP_EXECUTABLE="pup.py"
PUP_URL="https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.py"


get_pup() {
  DIR="$PIXI_PUP_HOME"
  while [ "$DIR" != "/" ]; do
    echo "👀 for pup in $DIR ..."
    if [ -f "$DIR/pup.py" ]; then
      echo "🐶 woof! pup.py found in $DIR"
      PUP_FOUND=1
      PIXI_PUP_HOME=$DIR
      break
    fi
    DIR=$(dirname $DIR)
  done
  
  PUP_PATH="$PIXI_PUP_HOME/$PUP_EXECUTABLE"
  if [ -f $PUP_FOUND ]; then
    curl -fsSL $PUP_URL | grep -vE "^#!" > "$PUP_PATH"
    echo "🐶 woof! $PUP_PATH has arrived"
  fi
  chmod +x "$PUP_PATH"
}
get_pup


get_pixi() {
  if ! command -v pixi &> /dev/null; then
    curl -fsSL $PIXI_INSTALL_URL | bash
    source ~/.bashrc  # for GHA
    echo "✨ $(pixi -V) installed"
  else
    echo "✨ $(pixi -V) found"
  fi
}
get_pixi

pixi_init() {
  if [ -f "$PIXI_PUP_HOME/pixi.toml" ]; then
    echo "✨ here be pixies! pixi.toml found in $PIXI_PUP_HOME"
  else
    pixi init "$PIXI_PUP_HOME"
  fi
}
pixi_init

get_python_uv_click() {
  if [ -n "$1" ]; then
    # if a version is passed as argument, update/reinstall
    PY_VERSION="$1"
    INSTALL=1  
  else
    if ! command -v "$PIXI_PUP_HOME"/.pixi/envs/default/bin/python &> /dev/null; then
    # if no argument and no python, prompt w/default for non-interactive shell & install
      read -ei "$DEFAULT_PY_VERSION" -p \
        "Enter desired base Python version (supported: 3.10|3.11|3.12; blank=latest): " PY_VERSION
      INSTALL=1
    else
      INSTALL=0
    fi
  fi

  if [ $INSTALL -eq 1 ]; then
    pixi add python${PY_VERSION:+=$PY_VERSION}
    pixi add uv && echo "🟣 $(pixi run uv --version)"
    pixi add click
  else
    echo "🐍 python lives here!"
  fi
  pixi run python -VV
  PYTHON_EXECUTABLE=$(pixi run python -c 'import sys; print(sys.executable)')
  SHEBANG="#!$PYTHON_EXECUTABLE"
  if ! head -n 1 "$PUP_PATH" | grep -q "$SHEBANG"; then
    sed -i "1i $SHEBANG\n" "$PUP_PATH"
  fi
} 
get_python_uv_click "$1"


# # you source this file instead of running it, alias "pup" becomes available
# # `source pup.sh` or `. pup.sh` or
# # `. <(curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh)`
# # or just the last line
# # `. <(curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh | tail -1)`
pup() { DIR=$(pwd); while [ "$DIR" != "/" ] && [ ! -f "$DIR/pup.py" ]; do DIR=$(dirname "$DIR"); done; "$DIR/pup.py" "$@"; }
