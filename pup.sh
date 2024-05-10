# This is the installation Bash script for Puppy.

# IMPORTANT: pup will never touch or modify your system python.
# Except for Pixi, nothing is permanently placed on PATH.
# The base python installation and all virtual environments will
# reside in one folder, the one from which you call this script.

# From a folder that will become your pup/python home, call:

# curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh

# This script checks for the tools that pup requires and installs or updates them.
# It will ask for the desired python version and use the latest versions of the other tools.

# 1) pixi (see https://pixi.sh to learn more about Pixi)
# 2) base python (strictly one per pup/py home)
# 3) uv (see https://github.com/astral-sh/uv to learn more about uv)
# 4) click (see https://github.com/pallets/click to learn more about click)
# 5) pup.py

# In the final step, the script will export an alias "pup" pointed to "./pup.py".
# This alias is not permanent, by design, to easily between different base pup/pythons.
# Whenever you open a new terminal, simply call this script again to recreate the alias.
# Running this script from another folder will setup/activate another pup/python base.
# If another base python is needed, simply run this script again from another folder.
# Though it may work, it is not recommended to nest pup/py folders.

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
PIXI_PUP_HOME=$(pwd)
PUP_EXECUTABLE="pup.py"
PUP_URL="https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.py"

get_pixi() {
  if ! command -v pixi &> /dev/null; then
    curl -fsSL $PIXI_INSTALL_URL | bash
  else
    echo "✨ $(pixi -V) found"
  fi
}

pixi_init() {
  DIR="$PIXI_PUP_HOME"
  FOUND_PIXI_OR_PUP=0
  while [ "$DIR" != "/" ]; do
    echo 👀 for pups and pixies in "$DIR" ...
    if [ -f "$DIR/pixi.toml" ] || [ -f "$DIR/pup.py" ]; then
      echo "✨ here be pixies: $DIR"
      FOUND_PIXI_OR_PUP=1
      break
    fi
    DIR=$(dirname $DIR)
  done
  [[ $FOUND_PIXI_OR_PUP -eq 0 ]] && pixi init . || PIXI_PUP_HOME="$DIR"
  echo $PIXI_PUP_HOME
}

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
    pixi add uv
    pixi add click
  else
    echo "python lives here!"
  fi
  pixi run python -VV
  PYTHON_EXECUTABLE=$(pixi run python -c 'import sys; print(sys.executable)')
  SHEBANG="#!$PYTHON_EXECUTABLE"
}

get_pup() {
  PUP_PATH="$PIXI_PUP_HOME/$PUP_EXECUTABLE"
  if ! [ -f "$PUP_PATH" ]; then
    echo "$SHEBANG" > "$PUP_PATH"
    curl -fsSL $PUP_URL >> "$PUP_PATH"
  else
    if ! head -n 1 "$PUP_PATH" | grep -q "$SHEBANG"; then
      echo "shebang!"
      sed -i "1i $SHEBANG" "$PUP_PATH"
    fi
  fi
  if ! [ -x "$PUP_PATH" ]; then
    chmod +x "$PUP_PATH"
  fi
  echo "🐶 woof!"
}


get_pixi
pixi_init
get_python_uv_click "$1"
get_pup

# you source this file instead of running it, alias "pup" becomes available
# `source pup.sh` or `. pup.sh` or
# `. <(curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh)`
pup() { "$PUP_PATH" "$@"; }