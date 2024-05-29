# Puppy

Your new best friend will help you set up python, with a little help from some powerful friends.

<img src="https://github.com/liquidcarbon/puppy/assets/47034358/da604ebd-4ce3-4e5d-b88b-ef46de7367fc" width="270">

## What does puppy do?

https://github.com/liquidcarbon/puppy/assets/47034358/16821b3b-f049-4e0a-873b-f90fcdc3f5a2

TLDR: `pup fetch` <-> `pip install`.  But wait, there's more!

There is a script called `pup`.  It's a cute little wrapper around **[pixi](https://github.com/prefix-dev/pixi)** and **[uv](https://github.com/astral-sh/uv)**, two modern and powerful Rust-based tools that complement each other.

### [LOL WHY](https://github.com/liquidcarbon/puppy/discussions/1)?

## Get started

To start, you need only `curl`/`iwr`; pup and friends will handle the rest.

The first command installs Pixi, Pup, and Python.
The second command creates alias `pup` in the current shell by sourcing the last line of the install script (do inspect the last line to ensure you trust it).

Everything is fetched into one folder, in complete isolation from system or any other python on your system.  Nothing (except Pixi) goes on PATH.

### Linux

```bash
curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh | bash
```

```bash
. <(curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh | tail -1)
```

### Windows

```powershell
iex (iwr https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.ps1).Content
```

```powershell
iex ((iwr https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.ps1).Content -split "`n")[-2]
```
> [!TIP] 
> Do inspect that last line to ensure you trust it.

### Check Installation
With `pup` alias:

```bash
$ pup --help
Usage: pup.py [OPTIONS] COMMAND [ARGS]...

  Call pup and friends for all your python needs.

Options:
  --help  Show this message and exit.

Commands:
  fetch   Fetch (install) packages with uv.
  kernel  Interactively create new ipython kernel linked to 🐶's environment.
  list    List packages.
  new     Create a new virtual environment in <WHERE> folder.
  play    Launch jupyter notebook with added code cells.
  which   Show 🐶's current home.
```

```bash
$ pup which
[2024-05-13 18:54:12] 🐶 says: home is /mnt/c/Users/a/Desktop/code/puppy513
```

```powershell
PS C:\Users\a\puppytest> pup which
[2024-05-13 18:48:16] 🐶 says: home is C:\Users\a\puppytest
```

> [!NOTE] 
> If you don't set the `pup` alias, Bash `./pup.py` will work thanks to a shebang; but for Powershell you'll have to find python executable and run `.\.pixi\envs\default\python.exe pup.py which`.

### File structure

A pup/py home is defined by one and only one python executable, which is managed by pixi,
along with tools like uv, jupyter, hatch, pytest, and conda-managed packages.
We use home-specific tools through a pixi shell from anywhere within the folder,
e.g. `pixi run python`, `pixi run jupyter`, or by calling their absolute paths.

```
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
```

### Install specific python version
```bash
curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh | bash -s 3.11
```

```powershell
& ([scriptblock]::Create((iwr -useb https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.ps1).Content)) 3.11
```

## Then what?

Check out usage [examples](https://github.com/liquidcarbon/puppy/tree/main/examples) and [workflows](https://github.com/liquidcarbon/puppy/tree/main/.github/workflows).

#### Generate environments, notebook kernels, and notebooks from CLI
[Screencast from 2024-05-24 15-35-33.webm](https://github.com/liquidcarbon/puppy/assets/47034358/272aea05-01c6-49c9-ada2-180cfac08927)

## Future
- `pup build` (via compile, freeze, etc.)
- `pup swim` (build [Dockerfiles](https://huggingface.co/spaces/liquidcarbon/pup-fileserver))


## Past
- the [first iteration](https://github.com/liquidcarbon/puppy/tree/b474b1cd6c63b9fc80db5d81f954536a58aeab2a) was a big Bash script

Thanks for checking out this repo.  Hope you try it out and like it!  Feedback, discussion, and ⭐s are welcome!
