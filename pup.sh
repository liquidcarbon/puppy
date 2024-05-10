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

echo $0

PIXI_INSTALL_URL="https://pixi.sh/install.sh"

get_pixi() {
  if ! command -v pixi &> /dev/null; then
    curl -fsSL $PIXI_INSTALL_URL | bash
  else
    echo "✨ $(pixi -V) found"
  fi
}

pixi_init() {
  if ! [ -f "pixi.toml" ] && ! [ -f "pyproject.toml" ]; then
    pixi init .
  else
    echo "✨ here be pixies"
  fi
}

get_python() {
  if [ -z "$1" ]; then
    if ! command -v .pixi/envs/default/bin/python &> /dev/null; then
      read -ei "3.12" -p "Enter desired base Python version (supported: 3.10|3.11|3.12; blank=latest): " PY_VERSION
      INSTALL=1  # if no python, prompt and install
    else
      echo "python lives here!"
    fi
  else
    PY_VERSION="$1"
    INSTALL=1  # if python exists but a version is passed as argument, update/reinstall
  fi
  # echo $PY_VERSION
  [[ -z "$INSTALL" ]] && pixi add python ${PY_VERSION:+=$PY_VERSION} uv click || pixi run python -VV
}

get_pixi
pixi_init
get_python "$1"
