<#
.SYNOPSIS
  Puppy Powershell install script.
.DESCRIPTION
    This script is used to install Puppy on Windows from the command line.

IMPORTANT: pup will never touch or modify your system python.
Except for Pixi, nothing is permanently placed on PATH.
The base python installation and all virtual environments will
reside in one folder, the one from which you call this script.

From a folder that will become your pup/python home, call:

iwr -useb https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.ps1 | iex

This script checks for the tools that pup requires and installs or updates them.
It will ask for the desired python version and use the latest versions of the other tools.

1) pup.py
2) pixi (see https://pixi.sh to learn more about Pixi)
3) base python (strictly one per pup/py home)
4) uv (see https://github.com/astral-sh/uv to learn more about uv)
5) click (see https://github.com/pallets/click to learn more about click)

In the final step, the script can export an alias "pup" pointed to "./pup.py".
This alias is not permanent, by design, to easily between different base pup/pythons.
Whenever you open a new terminal, simply call the last line of this script again to
recreate the alias.  Running this script from another folder will setup/activate another
pup/python base.  If another base python is needed, simply run this script again
from another folder.
Do not nest pup/py folders.

A pup/py home is defined by one and only one python executable, which is managed by pixi,
along with tools like uv, jupyter, hatch, pytest, and conda-managed packages.
We use home-specific tools through a pixi shell from anywhere within the folder,
e.g. `pixi run python`, `pixi run jupyter`, or by calling their absolute paths.

The blueprint for a pup/py home is in `pixi.toml`; at this level, git is not needed.
The inner folders are git-ready project environments managed by pup and uv.
In each of the inner folders, there is a classic `.venv` folder populated by uv, and
a `pyproject.toml` file that is kept in sync with the environment by pup.

├── puphome
│   ├── env1
│   │   ├── .venv
│   │   └── pyproject.toml
│   ├── env2
│   │   ├── .venv
│   │   └── pyproject.toml
│   ├── pixi.toml
│   └── pup.py
├── pup311torch
│   ├── env3
│   └── env4
└── pup313beta
    └── env5

────────────────────────────
Illustration of pup/py homes

.NOTES
    Version: v0.2.0
#>

$DEFAULT_PY_VERSION="3.12"
$PIXI_INSTALL_URL="https://pixi.sh/install.ps1"
$PIXI_PUP_HOME=$(pwd).Path  # initial assumption; will check parent paths
$PUP_EXECUTABLE="pup.py"
$PUP_URL="https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.py"


function get_pup {
  $PUP_FOUND=0
  $DIR = $PIXI_PUP_HOME
  while ($DIR -ne [System.IO.Path]::GetPathRoot($DIR)) {
    Write-Host "👀 for pup in $DIR ..."
    if (Test-Path "$DIR/$PUP_EXECUTABLE") {
      Write-Host "🐶 woof! pup.py found in $DIR"
      $PUP_FOUND=1
      $PIXI_PUP_HOME = $DIR
      break
    }
    $DIR = Split-Path $DIR
  }
  $PUP_PATH="$PIXI_PUP_HOME/$PUP_EXECUTABLE"
  if ($PUP_FOUND -ne 1) {
    (iwr -useb $PUP_URL).Content -split "`n" | ForEach-Object {
      if (-not $_.startsWith("#!")) { $_ }
      } | Out-File -FilePath $PUP_PATH -Encoding UTF8
    Write-Host "🐶 woof! $PUP_PATH has arrived"
  }
}
get_pup


function get_pixi {
  if (!(Get-Command -Name pixi -ErrorAction SilentlyContinue)) {
    iwr -useb  $PIXI_INSTALL_URL | iex
    Write-Host "✨ $(pixi -V) installed"
  }
  else {
    Write-Host "✨ $(pixi -V) found"
  }
}
get_pixi


function pixi_init {
  if (Test-Path "$PIXI_PUP_HOME/pixi.toml") {
    Write-Host "✨ here be pixies! pixi.toml found in $PIXI_PUP_HOME"
  }
  else {
    pixi init "$PIXI_PUP_HOME"
  }
}
pixi_init


function get_python_uv_click {
  param (
    [string]$PY_VERSION
  )
  if ($PY_VERSION) {
    # if a version is passed as argument, update/reinstall
    $INSTALL = 1
  }
  else {
    if (!(Test-Path "$PIXI_PUP_HOME/.pixi/envs/default/python.exe")) {
      # If no argument and no python, prompt w/default for non-interactive shell & install
      $DEFAULT_PY_VERSION = "3.12" # Update with your default Python version
      $PromptMessage = "Enter desired base Python version (supported: 3.10|3.11|3.12; blank=latest)"
      $PY_VERSION = Read-Host -Prompt $PromptMessage
      if (-not $PY_VERSION) { $PY_VERSION = $DEFAULT_PY_VERSION }
      $INSTALL = 1
    }
    else {
      $INSTALL = 0
    }
  }

  if ($INSTALL -eq 1) {
    pixi add "python=$PY_VERSION"
    pixi add uv; Write-Host "🟣 $(pixi run uv --version)"
    pixi add click
  }
  else {
    Write-Host "🐍 python lives here!"
  }
  pixi run python -VV
  $PYTHON_EXECUTABLE=$(pixi run python -c 'import sys; print(sys.executable)')
}

if ($args.Count -gt 0) {
    get_python_uv_click $args[0]
} else {
    get_python_uv_click $null  # make PS 5 happy
}


# you source this file instead of running it, alias "pup" becomes available
# or just the last line:
# iex (Get-Content https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.ps1 | Select-Object -Last 1)
function pup() { $DIR=$PWD; while (!(Test-Path "$DIR/pup.py") -and ($DIR -ne [System.IO.Path]::GetPathRoot($PWD))) { $DIR=Split-Path $DIR}; & "$DIR/.pixi/envs/default/python.exe" "$DIR/pup.py" @args; }
