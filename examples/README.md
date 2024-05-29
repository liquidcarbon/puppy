# Examples

## Generate notebooks by fetching external scripts

Check out [workflows](https://github.com/liquidcarbon/puppy/actions/runs/9277393540).

```bash
# install jupyter
pixi add jupyter nbclient

# create pup alias
. <(cat pup.sh | tail -1)

# create new venv, install packages
pup fetch ducks-pandas duckdb pandas

# create new jupyter kernel matching `ducks-pandas` environment
pup kernel ducks-pandas ducks-pandas-3.12

# create, run, and launch a notebook
PY_URL=https://raw.githubusercontent.com/liquidcarbon/puppy/main/examples/Q-strings/Q.py
pup play -k ducks-pandas-3.12 \
-c \"md|### 🐶 I can fetch external scripts into this notebook!;and run them\" \
-c \"\`curl -s $PY_URL\`\" \
-c \"Q('../examples/Q-strings/query1.sql', file=True, x=42).run()\" \
-N -S"
```