# Puppy
Your new best friend is quite fond of snakes and will guide you from zero python to complex environments, with a little help from some powerful friends.

<img src="https://github.com/liquidcarbon/puppy/assets/47034358/da604ebd-4ce3-4e5d-b88b-ef46de7367fc" width="270">

## What does puppy do?

There is one simple script called `pup`.  It's a cute little wrapper around **[pixi](https://github.com/prefix-dev/pixi)** and **[uv](https://github.com/astral-sh/uv)**, two modern and powerful Rust-based tools that complement each other.

### [LOL WHY](https://github.com/liquidcarbon/puppy/discussions/1)?

## Get started

1. Clone this repo to a folder to house all your future python needs
> [!TIP] 
> everything in this folder is completely isolated from previous python tools you may have, except for Pixi; to clean up, just delete the folder

2. Register `pup` on `PATH`
```bash
./pup  # if you don't want to pollute PATH, skip this and run below with "./pup" instead of "pup"
``` 

3. Summon Pixi to install uv, the specified python version, and any system tools or conda/mamba packages
```bash
pup py3.11
```
> [!TIP] 
> this is your base layer, packages you need globally go here, e.g. `pup py3.11 jupyter jupyter-collaboration` (works via `pixi add`)

4. Summon uv to install packages into a chosen environment with `pup fetch` (same as `pup install`).  Note the extra argument for `[WHERE]` to install. - to install into **base environment**:
```bash
pup fetch . duckdb pandas  # pup fetch [WHERE] [WHAT] [OPTIONS]
```
- to install into a **new environment** called `viz`, nested in the same folder:
```bash
pup fetch viz altair bokeh matplotlib seaborn
```
> [!NOTE]
> if there is Jupyter in the base layer, `pup` will make you a kernel with a matching name

5. Launch your main use case via configurable [Pixi tasks](https://pixi.sh/latest/advanced/advanced_tasks/)
```bash
pup play
```
- start Jupyter, with all kernels attached (default)
- launch Gradio / FastAPI / Panel app
- run any other script, similar to [Docker CMD](https://docs.docker.com/reference/dockerfile/#cmd) except you can have more than one.

## Future
- `pup build` (via compile, freeze, etc.)
- `pup swim` (build Dockerfiles)
