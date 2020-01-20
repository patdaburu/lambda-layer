#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 1/20/20
"""
Create packages using ``bash``.

.. currentmodule:: lambda_layer.package.bash
.. moduleauthor:: Pat Daburu <pat@daburu.net>
"""
import os
import shutil
from subprocess import Popen, PIPE
from pathlib import Path
import tempfile
from typing import Iterable, NamedTuple, Tuple, Union
import zipfile
import click
from lambda_layer.config import LayerConfig


class ProcOutput(NamedTuple):
    stdout: str
    stderr: str


def _run(
        cmd: Iterable[str],
        shell: bool = False,
        silent: bool = False
) -> ProcOutput:
    # If we're not running silent...
    if not silent:
        # ...echo the command.
        click.echo(' '.join(cmd))

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

    output = ProcOutput(
        stdout=stdout.decode('utf-8'),
        stderr=stdout.decode('utf-8')
    )

    fg = 'green' if proc.returncode == 0 else 'red'

    if stdout and proc.returncode != 0 or not silent:
        for line in stdout.decode('utf-8').split('\n'):
            click.echo(click.style(line, fg=fg))

    # If anything was printed to standard error, let's show that.
    if stderr:
        for line in stderr.decode('utf8').split('\n'):
            click.echo(click.style(line, fg='red'))

    return output


def _venv(
        # python: str,
        path: Path,  # TODO: just go with the path
        silent: bool = False
) -> Path:
    cmd = [
        'python', '-m', 'venv',  # TODO: Standardize this.
        str(path)
    ]

    _run(cmd, silent=silent)

    return path


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
        upgrade_pip: bool = True,
        silent: bool = False
):
    # Let's start preparing the install commands.  First up: activate
    # the virtual environment.
    cmds = [
        f"source {venv}/bin/activate"
    ]
    # Upgrade pip (if requested).
    if upgrade_pip:
        cmds.append("pip3 install --upgrade pip")
    # Install whatever is in the `requirements.txt`.
    cmds.append(f"pip3 install -r {requirements}")

    cmd = [' && '.join(cmds)]

    _run(cmd, shell=True, silent=silent)


def _site_packages(venv: str, silent: bool = False) -> Path:
    cmds = [
        f"source {venv}/bin/activate",
        'python -c "import site; print(site.getsitepackages())"'
    ]
    output = _run(
        cmd=[' && '.join(cmds)],
        shell=True,
        silent=silent
    )
    _path = Path(output.stdout[2:-3])
    return _path


def _archive(
        site_packages: Path,
        archive: Path
) -> Path:
    # We'll need the length of the `site_packages` path so we can remove
    # it from the archive names of files we place into the .zip archive.
    site_packages_len = len(str(site_packages))
    with zipfile.ZipFile(str(archive), 'w', zipfile.ZIP_DEFLATED) as zip:
        # ``zip`` is zipfile handle.
        for root, dirs, files in os.walk(str(site_packages)):
            for file in files:
                path = os.path.join(root, file)
                arcname = path[site_packages_len:]
                zip.write(path, arcname=arcname)

    return archive


def make(
        # python: str,
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
            # python=_python,
            path=(Path(tmp_path) / 'venv'),
            silent=silent
        )
        # Write the requirements file.
        requirements = _requirements(
            path=tmp_path / 'requirements.txt',
            packages=layer.packages
        )

        _install(venv=venv, requirements=requirements)

        # Get the path to the site packages directory.
        site_packages = _site_packages(venv=venv, silent=silent)

        archive = _archive(
            # python=_python,
            site_packages=site_packages,
            archive=tmp_path / f"{layer.name}-{layer.version}.zip"
        )

        # TODO: Copy the file

        # Calculate the path to the final distribution archive.
        dist_path = _dist_dir / archive.name

        if not silent:
            click.echo(f"Copying  {archive} to {dist_path}")

        # Copy the archive to the distribution directory.
        shutil.copyfile(str(archive), str(dist_path))

        g = input("any key yo")


        # Return the path to the distribution file.
        return dist_path


