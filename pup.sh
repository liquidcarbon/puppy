# Runner / installer / updater for puppy v2.

#!/bin/bash

DEFAULT_PY_VERSION=3.13
GH_BRANCH=v2
GH_URL=https://raw.githubusercontent.com/liquidcarbon/puppy/"$GH_BRANCH"/
PIXI_INSTALL_URL=https://pixi.sh/install.sh

main() {
  DIR=$(pwd)
  while [ "$DIR" != "/" ]; do
    if [ -f "$DIR/pup.py" ]; then
      PUP="$DIR/pup.py"
      PUP_HOME="$DIR"
      break
    fi
    DIR=$(dirname "$DIR")
  done

  if [ -n $PUP ] && [ "$1" != "update" ]; then
    run "$@"
  elif [ -n $PUP ] && [ "$1" == "update" ]; then
    update
  else
    install "$@"
  fi
}

run() {
  PY="$PUP_HOME"/.pixi/envs/default/bin/python
  if [ -n "$PY" ]; then
    "$PY" "$PUP" "$@"
  else
    pixi run python "$PUP" "$@"
  fi
}

update() {
  get_pixi
  pixi self-update
  pixi update
  get_pup
}

install() {
  get_pixi
  pixi_init
  get_python_uv_click "$1"
  get_pup
}

get_pixi() {
  if ! command -v pixi &> /dev/null; then
    curl -fsSL $PIXI_INSTALL_URL | bash
    export PATH=$HOME/.pixi/bin:$PATH  # for GHA
    echo "✨ $(pixi -V) installed"
  else
    echo "✨ $(pixi -V) found"
  fi
  PIXI_HOME=$(dirname $(command -v pixi))
}

pixi_init() {
  if pixi run &> /dev/null; then
    echo "✨ here be pixies! pixi.toml found in $PIXI_PUP_HOME"
  else
    pixi init .
  fi
}

py_ver_prompt() {
  read -ei "$DEFAULT_PY_VERSION" -p "$(cat <<-EOF
Enter desired base Python version
(supported: 3.10|3.11|3.12|3.13; blank=latest):
EOF
)" PY_VERSION
}

get_python_uv_click() {
  if [ -n "$1" ]; then
    # if a version is passed as argument, update/reinstall
    PY_VERSION="$1"
    INSTALL=1  
  else
    if pixi run python -V &> /dev/null; then
      INSTALL=0
    else
      # no argument and no python? prompt w/default for non-interactive shell & install
      py_ver_prompt
      INSTALL=1
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
} 

get_pup() {
  curl "$GH_URL" -o pup.py
  curl "$GH_URL/pup.sh" -o "$PIXI_HOME/pup"
  chmod +x "$PIXI_HOME/pup"
  "$PIXI_HOME/pup" hi
}

main "$@"
