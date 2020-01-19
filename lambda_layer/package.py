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
from typing import Callable, Union
import click
from .config import LayerConfig


def _venv(
        parent: Path,
        silent: bool = False
) -> Path:
    _venv_path = parent / 'venv'
    cmd = [
        'python3', '-m', 'venv',
        str(_venv_path)
    ]  # TODO: Standardize this.

    proc = Popen(
        cmd,
        stdout=PIPE,
        stderr=PIPE
    )
    stdout, stderr = proc.communicate()

    fg = 'green' if proc.returncode == 0 else 'red'

    if proc.returncode != 0 or not silent:
        for line in stdout.decode('utf-8').split('\n'):
            click.echo(click.style(line, fg=fg))

    if not _venv_path.is_dir():
        raise Exception(f"{_venv_path} was not created.")  # TODO: Custom exceptions

    return _venv_path


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
        venv_path = _venv(parent=Path(tmp_path), silent=silent)

        print(f"Created {venv_path}")
