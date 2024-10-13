# Puppy

Your new best friend will help you set up and organize your python projects, with a little help from some powerful friends.

<img src="https://github.com/liquidcarbon/puppy/assets/47034358/da604ebd-4ce3-4e5d-b88b-ef46de7367fc" width="270">

Puppy is a transparent wrapper around [pixi](https://github.com/prefix-dev/pixi/) and [uv](https://github.com/astral-sh/uv), two widely used Rust-based tools that belong together.

Puppy installs python, creates projects and virtual environments, and launches notebook properly linked to venvs. 

## Get started

To start, you need only `curl` / `iwr` and an empty folder; pup and friends will handle the rest.

### Linux

```bash
curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh | bash
```

### Windows

```powershell
iex (iwr https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.ps1).Content
```

## How It Works

Puppy preps the folder to house python, in complete isolation from system or any other python on your system:

0) 🐍 this folder is home to one and only one python executable, managed by pixi
1) ✨ pixi installs core components: python, uv, click
2) ⚙ [Bash](https://github.com/liquidcarbon/puppy/blob/main/pup.sh) or [Powershell](https://github.com/liquidcarbon/puppy/blob/main/pup.ps1) runner/installer is placed into `~/.pixi/bin` (the only folder that goes on PATH)
3) 🐶 `pup.py` is the python/[click](https://github.com/pallets/click) CLI that wraps pixi and uv commands
4) 🟣 `pup new` and `pup add` use uv to handle projects, packages and virtual environments
5) 🥳 `pup play` creates and launches notebooks (marimo or jupyter) properly linked to the virtual environments

## Notebooks

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

## Support

Thanks for checking out this repo.  Hope you try it out and like it!  Feedback, discussion, and ⭐s are welcome!