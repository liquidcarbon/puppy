# Runner / installer / updater for puppy v2.

#!/bin/bash

DEFAULT_PY_VERSION=3.12
GH_BRANCH=main
GH_URL=https://raw.githubusercontent.com/liquidcarbon/puppy/"$GH_BRANCH"/
PIXI_INSTALL_URL=https://pixi.sh/install.sh

main() {
  DIR=$(pwd)
  while [ "$DIR" != "/" ]; do
    [[ -f "$DIR/pixi.toml" ]] && PIXI_TOML="$DIR/pixi.toml"
    if [ -f "$DIR/pup.py" ]; then
      PUP="$DIR/pup.py"
      PUP_HOME="$DIR"
      break
    fi
    DIR=$(dirname "$DIR")
  done

  if [ -f $PUP ] && [ "$1" != "update" ]; then
    echo RUN
    run "$@"
  elif [ -f $PUP ] && [ "$1" == "update" ]; then
    update
  else
    install "$@"
  fi
}

run() {
  PY="$PUP_HOME"/.pixi/envs/default/bin/python
  if [ -e "$PY" ]; then
    "$PY" "$PUP" "$@"
  else
    if ! pixi run python "$PUP" "$@"; then
      install "$@"
    fi
  fi
}


update() {
  get_pixi
  pixi self-update
  pixi update
  get_pup
}


install() {
  if [ "$(ls -A)" != "" ]; then
    read -ei "y" -p \
      "$(pwd) is not empty; do you want to make it puppy's home? (y/n): "
      [[ "$REPLY" == "n" ]] && exit 1
  fi
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
  if [ -f "$PUP_HOME/pixi.toml" ]; then
    echo "✨ here be pixies! pixi.toml found"
  else
    pixi init .
  fi
}


py_ver_prompt() {
  if [ -t 0 ]; then
    read -ei "$DEFAULT_PY_VERSION" -p "$(cat <<-EOF
Enter desired base Python version
(supported: 3.9|3.10|3.11|3.12|3.13; blank=3.12):$(printf '\u00A0')
EOF
)" PY_VERSION
  else
    PY_VERSION="$DEFAULT_PY_VERSION"
  fi
}


get_python_uv_click() {
  if [ -n "$1" ]; then
    # if a version is passed as argument, update/reinstall
    PY_VERSION="$1"
    INSTALL=1
  else
    if grep -q python "$PUP_HOME/pixi.toml" &> /dev/null; then
      INSTALL=0
    else
      # no argument and no python? prompt w/default for non-interactive shell & install
      py_ver_prompt
      INSTALL=1
    fi
  fi
  if [ $INSTALL -eq 1 ]; then
    pixi add python${PY_VERSION:+=$PY_VERSION}
    pixi add "uv>=0" && echo "🟣 $(pixi run uv --version)"
    pixi add "click>=8"
    # using ">=" overrides pixi's default ">=,<" and allows updates to new major versions
  else
    echo "🐍 python lives here!"
  fi
  pixi run python -VV
  # PYTHON_EXECUTABLE=$(pixi run python -c 'import sys; print(sys.executable)')
}


get_pup() {
  if [ -n $PUP ] && [ -f "$PUP" ]; then
    curl -fsSL "$GH_URL/pup.py" -o "$PUP" && chmod +x "$PUP"
  else
    curl -fsSL "$GH_URL/pup.py" -o pup.py && chmod +x pup.py
  fi
  curl -fsSL "$GH_URL/pup.sh" -o "$PIXI_HOME/pup"
  chmod +x "$PIXI_HOME/pup"
  "$PIXI_HOME/pup" hi
}


main "$@"
