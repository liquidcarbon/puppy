# Puppy
Your new best friend will help you set up python, with a little help from some powerful friends.

<img src="https://github.com/liquidcarbon/puppy/assets/47034358/da604ebd-4ce3-4e5d-b88b-ef46de7367fc" width="270">

## What does puppy do?

There is one simple script called `pup`.  It's a cute little wrapper around **[pixi](https://github.com/prefix-dev/pixi)** and **[uv](https://github.com/astral-sh/uv)**, two modern and powerful Rust-based tools that complement each other.

### [LOL WHY](https://github.com/liquidcarbon/puppy/discussions/1)?

## Get started

To start, you need only `curl`; pup and friends will handle the rest.

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

## Detailed example with outputs

How long does it take to
- install python
- jupyter
- create two separate environments
- with matching Jupyter kernels
- and launch Jupyter?

Only 7 commands and less than 1 minute:

```bash
 ./pup
 pup py3.11 jupyter
 pup fetch . httpx
 pup fetch viz altair seaborn
 pup kernel . pup3.11-.
 pup kernel viz pup3.11-viz
 pup play
```

**Kernel 1** (🐶 base environment):
<img src="https://github.com/liquidcarbon/puppy/assets/47034358/ff8bc338-9298-4b09-b3b6-5fd3c6c8ffd4">

**Kernel 2** (viz):
<img src="https://github.com/liquidcarbon/puppy/assets/47034358/c2d08f29-3f12-48e9-9ade-1a39b15bdce5">



Here's what happened:

```bash
a@AK-Desktop-6600:~/code/puppy$ ./pup

 Usage: (each subcommand shows more help)
 pup
        initialize and link 🐶 to PATH
 pup py
        interactively install base python to current folder
        if you know what you need:
        pup py3.12 jupyter jupyter-collaboration>=2
        (additional arguments go into 'pixi add')
 pup fetch
        interactively install packages with uv into specified virtual env
        if you know what you need:
        pup fetch . duckdb
        pup fetch newviz altair seaborn
 pup install
        same as pup fetch
 pup home
        show 🐶's home folder
 pup kernel
        interactively create Jupyter kernel linked to 🐶's environment
        if you know what you need:
        pup kernel . pup3.11-home
        pup kernel dataenv pup3.11-data
 pup play
        runs PIXI_DEFAULT_TASK (default: 'jupyter notebook')
 pup whereami
        in case you got lost: log of 🐶's commands thus far
 pup which
        show 🐶's current symlink
 

# 2024-04-01T03:17:09 - woof!
# 2024-04-01T03:17:09 - 🐶 = /home/a/.local/bin/pup -> /home/a/code/puppy/pup
✔ Initialized project in /home/a/code/puppy
✔ Added task `start`: /home/a/code/puppy/.pixi/envs/default/bin/jupyter notebook --ip=0.0.0.0 --port=8880
a@AK-Desktop-6600:~/code/puppy$ pup py3.11 jupyter
# 2024-04-01T03:17:18 - 🐶 asked for: 'pixi add uv python=3.11 jupyter'
✔ Added uv
✔ Added python=3.11
✔ Added jupyter
# 2024-04-01T03:17:49 - ✨ Python 3.11.8 | packaged by conda-forge | (main, Feb 16 2024, 20:53:32) [GCC 12.3.0]
a@AK-Desktop-6600:~/code/puppy$ pup fetch . httpx
# 2024-04-01T03:18:00 - 🐶 asked for: 'pixi run uv pip install -p /home/a/code/puppy/.pixi/envs/default/bin/python httpx'
Audited 1 package in 74ms
a@AK-Desktop-6600:~/code/puppy$ pup fetch viz altair seaborn
Using Python 3.11.8 interpreter at: .pixi/envs/default/bin/python
Creating virtualenv at: viz/.venv
Activate with: source viz/.venv/bin/activate
# 2024-04-01T03:18:09 - pup & uv created new environment in viz
# 2024-04-01T03:18:09 - 🐶 asked for: 'pixi run uv pip install -p /home/a/code/puppy/viz/.venv/bin/python altair seaborn'
Resolved 24 packages in 146ms
Installed 24 packages in 58ms
 + altair==5.3.0
 + attrs==23.2.0
 + contourpy==1.2.0
 + cycler==0.12.1
 + fonttools==4.50.0
 + jinja2==3.1.3
 + jsonschema==4.21.1
 + jsonschema-specifications==2023.12.1
 + kiwisolver==1.4.5
 + markupsafe==2.1.5
 + matplotlib==3.8.3
 + numpy==1.26.4
 + packaging==24.0
 + pandas==2.2.1
 + pillow==10.2.0
 + pyparsing==3.1.2
 + python-dateutil==2.9.0.post0
 + pytz==2024.1
 + referencing==0.34.0
 + rpds-py==0.18.0
 + seaborn==0.13.2
 + six==1.16.0
 + toolz==0.12.1
 + tzdata==2024.1
(reverse-i-search)`kern': jupyter ^Crnelspec remove pup-viz pup-vizz
a@AK-Desktop-6600:~/code/puppy$ pup kernel
Usage: pup kernel [WHERE] [KERNEL_NAME]
Install kernel for which environment? .
Unique kernel name? (allowed characters: [a-zA-Z0-9.-_]) pup3.11.8-.
# 2024-04-01T03:18:35 - 🐶 asked for: 'pup kernel . pup3.11.8-.'
# 2024-04-01T03:18:36 - 🐶 asked for: 'pixi run uv pip install -p /home/a/code/puppy/.pixi/envs/default/bin/python ipykernel'
Audited 1 package in 23ms
# 2024-04-01T03:18:36 - 🐶 asked for: '/home/a/code/puppy/.pixi/envs/default/bin/python -m ipykernel install --user --name pup3.11.8-.'
0.00s - Debugger warning: It seems that frozen modules are being used, which may
0.00s - make the debugger miss breakpoints. Please pass -Xfrozen_modules=off
0.00s - to python to disable frozen modules.
0.00s - Note: Debugging will proceed. Set PYDEVD_DISABLE_FILE_VALIDATION=1 to disable this validation.
Installed kernelspec pup3.11.8-. in /home/a/.local/share/jupyter/kernels/pup3.11.8-.
a@AK-Desktop-6600:~/code/puppy$ pup kernel viz pup3.11-viz
# 2024-04-01T03:19:00 - found existing uv virtual environment viz
# 2024-04-01T03:19:00 - 🐶 asked for: 'pixi run uv pip install -p /home/a/code/puppy/viz/.venv/bin/python ipykernel'
Resolved 29 packages in 123ms
Installed 26 packages in 75ms
 + asttokens==2.4.1
 + comm==0.2.2
 + debugpy==1.8.1
 + decorator==5.1.1
 + executing==2.0.1
 + ipykernel==6.29.4
 + ipython==8.23.0
 + jedi==0.19.1
 + jupyter-client==8.6.1
 + jupyter-core==5.7.2
 + matplotlib-inline==0.1.6
 + nest-asyncio==1.6.0
 + parso==0.8.3
 + pexpect==4.9.0
 + platformdirs==4.2.0
 + prompt-toolkit==3.0.43
 + psutil==5.9.8
 + ptyprocess==0.7.0
 + pure-eval==0.2.2
 + pygments==2.17.2
 + pyzmq==25.1.2
 + stack-data==0.6.3
 + tornado==6.4
 + traitlets==5.14.2
 + typing-extensions==4.10.0
 + wcwidth==0.2.13
# 2024-04-01T03:19:00 - 🐶 asked for: '/home/a/code/puppy/viz/.venv/bin/python -m ipykernel install --user --name pup3.11-viz'
Installed kernelspec pup3.11-viz in /home/a/.local/share/jupyter/kernels/pup3.11-viz
a@AK-Desktop-6600:~/code/puppy$ pup play
✨ Pixi task (default): /home/a/code/puppy/.pixi/envs/default/bin/jupyter notebook --ip=0.0.0.0 --port=8880
```


## Future
- `pup build` (via compile, freeze, etc.)
- `pup swim` (build Dockerfiles)

Thanks for checking out this repo.  Feedback, discussion, and ⭐s are welcome!