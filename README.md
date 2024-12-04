# Puppy

Your new best friend will help you set up and organize your python projects, with a little help from some powerful friends.

<img src="https://github.com/liquidcarbon/puppy/assets/47034358/da604ebd-4ce3-4e5d-b88b-ef46de7367fc" width="270">

Puppy is a transparent wrapper around [pixi](https://github.com/prefix-dev/pixi/) and [uv](https://github.com/astral-sh/uv), two widely used Rust-based tools that belong together.

Puppy installs python, creates projects and virtual environments, and launches [marimo](https://github.com/marimo-team/marimo) or jupyter notebooks properly linked to venvs.

## Get started

To start, you need only `curl` / `iwr` and an empty folder; pup and friends will handle the rest.

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
  - virtual environments: [all other query parameters with comma-separated package names](https://pup-py-fetch.hf.space?env1=duckdb,pandas&env2=cowsay)

> [!NOTE]
> As of Dec 2024, many packages still do not support python 3.13; thus, the default version in puppy is 3.12.


Visiting the URLs above returns the installation scripts.  You can mix and match query parameters, unlocking single-command recipes for complex builds:

```bash
curl -fsSL "https://pup-py-fetch.hf.space?pixi=marimo&env1=duckdb,pandas&env2=cowsay" | bash
```

```powershell
iex (iwr "https://pup-py-fetch.hf.space?python=3.11&pixi=marimo&tables=duckdb,pandas,polars").Content
```

## How It Works

Puppy can be used as a CLI or as a module.

Installing puppy preps the folder to house python, in complete isolation from system or any other python on your system:

0) 🐍 this folder is home to one and only one python executable, managed by pixi
1) ✨ pixi installs core components: python, uv, click
2) ⚙ [Bash](https://github.com/liquidcarbon/puppy/blob/main/pup.sh) or [Powershell](https://github.com/liquidcarbon/puppy/blob/main/pup.ps1) runner/installer is placed into `~/.pixi/bin` (the only folder that goes on PATH)
3) 🐶 `pup.py` is the python/[click](https://github.com/pallets/click) CLI that wraps pixi and uv commands
4) 🟣 `pup new` and `pup add` use uv to handle projects, packages and virtual environments
5) 📀 `pup clone` and `pup sync` help build environments from external `pyproject.toml` project files

## Using `pup` as a Module

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

## Notebooks (WIP)

Coming soon: templates for Jupyter and Marimo notebooks.
[Unified environment management for any computational notebooks](https://github.com/marimo-team/marimo/discussions/2994) - no more Jupyter kernels!

`pup play --help`

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
