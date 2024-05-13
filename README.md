# Puppy

Your new best friend will help you set up python, with a little help from some powerful friends.

<img src="https://github.com/liquidcarbon/puppy/assets/47034358/da604ebd-4ce3-4e5d-b88b-ef46de7367fc" width="270">

## What does puppy do?

TLDR: `pup fetch` <-> `pip install`.  But wait, there's more!

There is a script called `pup`.  It's a cute little wrapper around **[pixi](https://github.com/prefix-dev/pixi)** and **[uv](https://github.com/astral-sh/uv)**, two modern and powerful Rust-based tools that complement each other.

### [LOL WHY](https://github.com/liquidcarbon/puppy/discussions/1)?

## Get started

To start, you need only `curl`/`iwr`; pup and friends will handle the rest.

The first command is the non-interactive installer.
The second command creates alias "pup" in the current shell by sourcing the last line of the install script (do inspect the last line to ensure you trust it).

### Linux

```bash
curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh | bash
```

```bash
. <(curl -fsSL https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.sh | tail -1)
```

### Windows

```powershell
iwr -useb https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.ps1 | iex
```

```powershell
iex (Get-Content https://raw.githubusercontent.com/liquidcarbon/puppy/main/pup.ps1 | Select-Object -Last 1)
```
> [!TIP] 
> Do inspect that last line to ensure you trust it.


## Then what?

Coming soon

## Future
- `pup build` (via compile, freeze, etc.)
- `pup swim` (build [Dockerfiles](https://huggingface.co/spaces/liquidcarbon/pup-fileserver))


## Past
- the [first iteration](https://github.com/liquidcarbon/puppy/tree/b474b1cd6c63b9fc80db5d81f954536a58aeab2a) was a big Bash script

Thanks for checking out this repo.  Hope you try it out and like it!  Feedback, discussion, and ⭐s are welcome!
