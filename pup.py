# -*- coding: utf-8 -*-
__doc__ = """
The CLI for pup, a cute python project manager.
"""

import sys

import click


class Pup:
    FILE: str = __file__
    LOG_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    PYTHON: str = sys.executable

    @classmethod
    def pedigree(cls):
        return f"pedigree: {cls.PYTHON} {cls.FILE}"


@click.group
def main():
    """Call pup and friends for all your python needs."""
    pass


@main.command(name="hi")
def say_hi():
    """Say hi to pup"""
    click.echo("🐶 says: woof!")


if __name__ == "__main__":
    main()
