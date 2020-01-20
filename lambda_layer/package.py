#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 1/19/20
"""
Create AWS lambda layer packages.

.. currentmodule:: lambda_layer.package
.. moduleauthor:: Pat Daburu <pat@daburu.net>
"""
from subprocess import Popen, PIPE
import sys
from pathlib import Path
import tempfile
from typing import Callable, Iterable, Union
import click
from .config import LayerConfig


def _run(
        cmd: Iterable[str],
        shell: bool = False,
        silent: bool = False
):
    print(' '.join(cmd))

    if shell:
        proc = Popen(
            list(cmd),
            stdout=PIPE,
            stderr=PIPE,
            shell=shell,
            executable='/bin/bash'  # TODO: Make this configurable!  (Or put it into the config!)
        )
    else:
        proc = Popen(
            list(cmd),
            stdout=PIPE,
            stderr=PIPE
        )
    stdout, stderr = proc.communicate()

    fg = 'green' if proc.returncode == 0 else 'red'

    if proc.returncode != 0 or not silent:
        for line in stdout.decode('utf-8').split('\n'):
            click.echo(click.style(line, fg=fg))

    # If anything was printed to standard error, let's show that.
    for line in stderr.decode('utf8').split('\n'):
        click.echo(click.style(line, fg='red'))


def _venv(
        path: Path,  # TODO: just go with the path
        silent: bool = False
) -> Path:
    cmd = [
        'python3', '-m', 'venv',  # TODO: Standardize this.
        str(path)
    ]

    _run(cmd, silent=silent)

    return path

    # proc = Popen(
    #     cmd,
    #     stdout=PIPE,
    #     stderr=PIPE
    # )
    # stdout, stderr = proc.communicate()
    #
    # fg = 'green' if proc.returncode == 0 else 'red'
    #
    # if proc.returncode != 0 or not silent:
    #     for line in stdout.decode('utf-8').split('\n'):
    #         click.echo(click.style(line, fg=fg))
    #
    # # If anything was printed to standard error, let's show that.
    # for line in stderr.decode('utf-8').split('\n'):
    #     click.echo(click.style(line, fg='red'))
    #
    # # At this point the directory should exist.
    # if not path.is_dir():
    #     raise Exception(f"{path} was not created.")  # TODO: Custom exceptions
    #
    # # Return the path to the virtual environment to the caller.
    # return path


def _requirements(
        path: Path,
        packages: Iterable[str],
        silent: bool = False
) -> Path:
    _path = path.expanduser().resolve()
    with open(str(_path), 'a') as fb:
        for package in packages:
            fb.write(f"{package}\n")
    # Return the file path to the caller.
    return _path


def _install(
        venv: Path,
        requirements: Path,
        silent: bool = False
):
    # TODO: Standardize this.
    cmd = [
        #'source', f"{venv}/bin/activate",  # '&&',
        # 'pip3', 'install', '-r', str(requirements)
        f"source {venv}/bin/activate && "
        f"pip3 install --upgrade pip && "  # TODO... this should be optional
        f"pip3 install -r {requirements}"
    ]

    _run(cmd, shell=True, silent=silent)


def make(
        dist_dir: Union[str, Path],
        layer: LayerConfig,
        silent: bool = False
) -> Path:
    # Prepare the distribution directory.
    _dist_dir = (
        dist_dir if isinstance(dist_dir, Path) else Path(dist_dir)
    ).expanduser().resolve()
    # The distribution directory must be a directory.
    if _dist_dir.is_file():
        raise IsADirectoryError(f"{_dist_dir} is not a directory.")
    # Create the distribution directory if it doesn't exist.
    _dist_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir).expanduser().resolve()
        # Create the virtual environment.
        venv = _venv(
            path=(Path(tmp_path) / 'venv'),
            silent=silent
        )
        # Write the requirements file.
        requirements = _requirements(
            path=tmp_path / 'requirements.txt',
            packages=layer.packages
        )

        _install(venv=venv, requirements=requirements)

        print(f"Created {venv}")

        g = input("any key yo")