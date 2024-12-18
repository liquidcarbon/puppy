# Puppy

Puppy helps you set up and manage your python projects.  It's the easiest way to get started with modern python on any platform, install packages in virtual environments, and contribute to external projects.

<img alt="Puppy Logo" src="https://github.com/liquidcarbon/puppy/assets/47034358/da604ebd-4ce3-4e5d-b88b-ef46de7367fc" width="270">


## Get started

https://github.com/user-attachments/assets/9cdd5173-5358-404a-84cc-f569da9972f8 

You need only `curl` / `iwr` and an empty folder; pup will handle the rest, with a little help from its powerful friends [pixi](https://github.com/prefix-dev/pixi/) and [uv](https://github.com/astral-sh/uv).


### Linux

```bash
curl -fsSL https://pup-py-fetch.hf.space | bash
```


### Windows

```powershell
iex (iwr https://pup-py-fetch.hf.space).Content
```


### One Installer To Rule Them All

The `pup-py-fetch` API accepts query parameters that allow specifying the exact environment recipe you want to build:
  - `python`: [3.10](https://pup-py-fetch.hf.space?python=3.10) through [3.13](https://pup-py-fetch.hf.space?python=3.13)
  - `pixi`: [comma-separated list of pixi/Conda dependencies](https://pup-py-fetch.hf.space?pixi=jupyter,quarto)
  - `clone`: [comma-separated list of GitHub repos to clone and install](https://pup-py-fetch.hf.space?clone=marimo-team/marimo) (only GitHub at this time)
  - virtual environments: [all other query parameters with comma-separated package names](https://pup-py-fetch.hf.space?env1=duckdb,pandas&env2=cowsay), including:
    - regular PyPI packages (no support for version pinning at this time)
    - packages from GitHub repos using <username>/<reponame>

> [!NOTE]
> As of Dec 2024, many packages still do not support python 3.13; thus, the default version in puppy is 3.12.


The URLs above return installation scripts.  You can mix and match query parameters, unlocking single-command recipes for complex builds:

```bash
curl -fsSL "https://pup-py-fetch.hf.space?pixi=marimo&env1=duckdb,pandas&env2=cowsay" | bash
```

```powershell
iex (iwr "https://pup-py-fetch.hf.space?python=3.11&pixi=marimo&tables=duckdb,pandas,polars").Content
```


## How It Works

Puppy is a transparent wrapper around [pixi](https://github.com/prefix-dev/pixi/) and [uv](https://github.com/astral-sh/uv), two widely used Rust-based tools that belong together.

Puppy can be used as a CLI in a Linux or Windows shell, or as a [module](#using-pup-as-a-module-pupfetch) in any python shell/script/[notebook](#puppy--environments-in-notebooks).

Installing puppy preps the folder to house python, in complete isolation from system or any other python on your system:

0) 🐍 this folder is home to one and only one python executable, managed by pixi
1) ✨ puppy installs pixi; pixi installs core components: python, uv, [click](https://github.com/pallets/click)
2) ⚙ [Bash](https://github.com/liquidcarbon/puppy/blob/main/pup.sh) or [Powershell](https://github.com/liquidcarbon/puppy/blob/main/pup.ps1) runner/installer is placed into `~/.pixi/bin` (the only folder that goes on PATH)
3) 🐶 `pup.py` is the python/click CLI that wraps pixi and uv commands
4) 🟣 `pup new` and `pup add` use uv to handle projects, packages and virtual environments
5) 📀 `pup clone` and `pup sync` help build environments from external `pyproject.toml` project files



## Using `pup` as a Module: `pup.fetch`

Pup can help you construct and activate python projects interactively, such as from (i)python shells, jupyter notebooks, or [marimo notebooks](https://github.com/marimo-team/marimo/discussions/2994).

```
a@a-Aon-L1:~/Desktop/puppy$ .pixi/envs/default/bin/python
Python 3.12.7
>>> import pup; pup.fetch()
[2024-10-26 16:50:37] 🐶 said: woof! run `pup.fetch()` to get started
[2024-10-26 16:50:37] 🐶 virtual envs available: ['tbsky', 't1/web', 't2', 'tmpl', 'test-envs/e1']
Choose venv to fetch: t1/web
[2024-10-26 16:51:56] 🐶 heard: pup list t1/web
{
  "t1/web": [
    "httpx>=0.27.2",
    "requests>=2.32.3"
  ]
}
[2024-10-26 16:51:56] fetched packages from 't1/web': /home/a/Desktop/puppy/t1/web/.venv/lib/python3.12/site-packages added to `sys.path`
```

Now the "kernel" `t1/web` is activated.  In other words, packages installed `t1/web/.venv` are available on `sys.path`.

Need to install more packages on the go, or create a new venv?  Just provide the destination, and list of packages.

```python
pup.fetch("t1/web", "awswrangler", "cloudpathlib")
pup.fetch("data", "duckdb", "polars", root=True)
```

Here is the signature of `pup.fetch()`:
```python
def fetch(
    venv: str | None = None,
    *packages: Optional[str],
    site_packages: bool = True,
    root: bool = False,
) -> None:
    """Create, modify, or fetch (activate) existing venvs.

    Activating an environment means placing its site-packages folder on `sys.path`,
    allowing to import the modules that are installed in that venv.

    `venv`: folder containing `pyproject.toml` and installed packages in `.venv`
        if venv does not exist, puppy will create it, install *packages,
        and fetch newly created venv
    `*packages`: names of packages to `pup add`
    `site_packages`: if True, appends venv's site-packages to `sys.path`
    `root`: if True, appends venv's root folder to `sys.path`
        (useful for packages under development)
    """
```

With `root=True`, you also add new project's root folder to your environment, making its modules available for import.
This is useful for working with projects that themselves aren't yet packaged and built.
You also have the option to omit the site-packages folder with `site_packages=False`.

```
pixi run python
Python 3.12.7 | packaged by conda-forge | (main, Oct  4 2024, 16:05:46) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pup; pup.fetch("test-only-root", root=True, site_packages=False)
[2024-11-22 13:10:49] 🐶 said: woof! run `pup.fetch()` to get started
[2024-11-22 13:10:49] 🐶 virtual envs available: ['gr']
[2024-11-22 13:10:49] 🐶 heard: pup new test-only-root
[2024-11-22 13:10:49] 🐶 said: pixi run uv init /home/a/puppy/test-only-root -p /home/a/puppy/.pixi/envs/default/bin/python --no-workspace
Initialized project `test-only-root` at `/home/a/puppy/test-only-root`
[2024-11-22 13:10:49] 🐶 said: pixi run uv venv /home/a/puppy/test-only-root/.venv -p /home/a/puppy/.pixi/envs/default/bin/python
Using CPython 3.12.7 interpreter at: .pixi/envs/default/bin/python
Creating virtual environment at: test-only-root/.venv
Activate with: source test-only-root/.venv/bin/activate
Specify what to install:
[2024-11-22 13:10:50] 🐶 virtual envs available: ['gr', 'test-only-root']
[2024-11-22 13:10:50] fetched packages from 'test-only-root': /home/a/puppy/test-only-root added to `sys.path`
[2024-11-22 13:10:50] 🐶 heard: pup list test-only-root
{
  "test-only-root": []
}
>>> import hello; hello.main()  # `hello.py` is included in uv's project template
Hello from test-only-root!
```

## Puppy & Environments in Notebooks

> [!NOTE]
> Conda or PyPI packages installed with `pixi add ...` always remain on `sys.path` and stay available across all environments.  Though one could exclude them, I have yet to find a reason to do so.

### Jupyter

There's a good chance you're confused about how Jupyter kernels work and find setting up kernels with virtual environments too complicated to bother.  Puppy's [v1](https://github.com/liquidcarbon/puppy/tree/v1) was addressing that problem, but in v2 (current version) this is taken care of by `pup.fetch`.  Here's the gist:

1) install ONE instance of jupyter with `pixi add jupyter` per major version of python
2) run it with `pixi run jupyter lab` or `pixi run jupyter notebook`
3) use `pup.fetch` to build and activate your environment - THAT'S IT!

For details, scan through the [previous section](#using-pup-as-a-module-pupfetch).  In brief, `pup.fetch` creates/modifies and/or activates your venv by appending its folder to `sys.path`.  This is pretty very similar to how venvs and kernels work. A jupyter kernel is a pointer to a python executable.  Within a venv, the executable `.venv/bin/python` is just a symlink to the parent python - in our case, to pixi's python.  The activation and separation of packages is achieved by manipulating `sys.path` to include local `site-packages` folder(s).


### Marimo

With marimo, you have more options: [Unified environment management for any computational notebooks](https://github.com/marimo-team/marimo/discussions/2994) - no more Jupyter kernels!


## Where Pixi Shines 🎇

UV is rightfully getting much love in the community, but Pixi is indispensable for:

1. Conda channels support
2. Setting up really complex build environments for multi-language projects.  For example, try pulling together what's done here in one API call (python, NodeJS, pnpm, cloned and synced repo): 
\
\
<img alt="Pixi build with python, Node, pnpm, and cloned repos" src="https://github.com/user-attachments/assets/b372b1a5-c3d6-415c-acb2-cc65d1f90572" width="480">


## Multi-Puppy-Verse

Can I have multiple puppies?  As many as you want!  Puppy is not just a package installer, but also a system to organize multiple python projects.

A pup/py home is defined by one and only one python executable, which is managed by pixi, along with tools like uv, jupyter, hatch, pytest, and conda-managed packages. We use home-specific tools through a pixi shell from anywhere within the folder, e.g. `pixi run python`, `pixi run jupyter`, or, to be explicit, by calling their absolute paths.

> [!NOTE]
> If you need a "kernel" with a different version of python, install puppy in a new folder.  **Puppy's folders are completely isolated from each other and any other python installation on your system.**  Remember, one puppy folder = one python executable, managed by Pixi.  Pup commands work the same from anywhere within a pup folder, run relative to its root, via `.pixi/envs/default/bin/python`.  Place puppy folders side-by-side, not within other puppy folders - nested puppies might misbehave.

```
# ├── puphome/  # python 3.12 lives here
# │   ├── public-project/
# │   │   ├── .git  # this folder may be a git repo (see pup clone)
# │   │   ├── .venv
# │   │   └── pyproject.toml
# │   ├── env2/
# │   │   ├── .venv/  # this one is in pre-git development
# │   │   └── pyproject.toml
# │   ├── pixi.toml
# │   └── pup.py
# ├── pup311torch/  # python 3.11 here
# │   ├── env3/
# │   ├── env4/
# │   ├── pixi.toml
# │   └── pup.py
# └── pup313beta/  # 3.13 here
#     ├── env5/
#     ├── pixi.toml
#     └── pup.py
```

The blueprint for a pup/py home is in `pixi.toml`; at this level, git is usually not needed.  The inner folders are git-ready project environments managed by pup and uv.  In each of the inner folders, there is a classic `.venv` folder and a `pyproject.toml` file populated by uv.  When you run `pup list`, pup scans this folder structure and looks inside each `pyproject.toml`.  The whole setup is very easy to [containerize](examples/) (command to generate `Dockerfile` coming soon!).

> [!TIP]
> Use `pup list -f` to list all dependencies spelled out in `uv.lock`.

## But Why

Python packages, virtual environments, notebooks, and how they all play together remains a confusing and controversial topic in the python world.

The problems began when the best idea from the Zen of python was ignored by pip:

```
~$ python -c 'import this'
The Zen of Python, by Tim Peters

...
Explicit is better than implicit.
...

~$ pip install numpy
Collecting numpy
  Downloading numpy-2.1.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (60 kB)
Downloading numpy-2.1.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.3/16.3 MB 62.5 MB/s eta 0:00:00
Installing collected packages: numpy
Successfully installed numpy-2.1.2
```

The command worked, yay! Antigravity!  But *which* pip did the work and *where* did the packages go?

![confused Travolta](https://i.kym-cdn.com/photos/images/newsfeed/001/042/619/4ea.jpg)

Most tools that came later followed the same pattern.

Puppy makes implicitly sensible choices while being explicitly transparent.  Compare:

```
PS C:\Users\a\Desktop\code\puppy> pup add try-ml numpy
[2024-10-13 00:02:19] 🐶 heard: pup new try-ml
[2024-10-13 00:02:19] 🐶 said: pixi run uv init C:\Users\a\Desktop\code\puppy\try-ml -p C:\Users\a\Desktop\code\puppy\.pixi\envs\default\python.exe --no-workspace
Initialized project `try-ml` at `C:\Users\a\Desktop\code\puppy\try-ml`
[2024-10-13 00:02:20] 🐶 said: pixi run uv venv C:\Users\a\Desktop\code\puppy\try-ml/.venv -p C:\Users\a\Desktop\code\puppy\.pixi\envs\default\python.exe
Using CPython 3.12.7 interpreter at: .pixi\envs\default\python.exe
Creating virtual environment at: try-ml/.venv
Activate with: try-ml\.venv\Scripts\activate
[2024-10-13 00:02:21] 🐶 heard: pup add try-ml numpy
[2024-10-13 00:02:21] 🐶 said: pixi run uv add numpy --project C:\Users\a\Desktop\code\puppy\try-ml
Resolved 2 packages in 87ms
Installed 1 package in 344ms
 + numpy==2.1.2
```

Then came Jupyter notebooks, a wonderful tool that unlocked the floodgates of interest to python.  But the whole `import` thing remained a confusing mess.

(to be continued)

## Future

- `pup swim` (build Dockerfiles)
- you tell me?

## Past

- [v0](https://github.com/liquidcarbon/puppy/tree/b474b1cd6c63b9fc80db5d81f954536a58aeab2a) was a big Bash script
- [v1](https://github.com/liquidcarbon/puppy/tree/v1) remains a functional CLI with `pup play` focused on Jupyter kernels

## Built with Puppy

See [examples](examples/README.md).

## Support

Thanks for checking out this repo.  Hope you try it out and like it!  Feedback, discussion, and ⭐s are welcome!
