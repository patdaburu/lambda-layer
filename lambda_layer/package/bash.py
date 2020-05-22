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
import sys
from pathlib import Path
import tempfile
from typing import Iterable, Union
import zipfile
import click
from .common import ProcOutput
from .. import env
from ..config import LayerConfig


def _run(
        cmd: Iterable[str],
        shell: bool = False,
        silent: bool = False
) -> ProcOutput:
    """
    Run a process.

    :param cmd: the command
    :param shell:  ``True`` to run in a full shell environment
    :param silent: ``True`` to suppress normal output
    """
    # If we're not running silent...
    if not silent:
        # ...echo the command.
        click.echo(' '.join(cmd))
    # If we're supposed to use a full shell...
    if shell:
        proc = Popen(
            list(cmd),
            stdout=PIPE,
            stderr=PIPE,
            shell=shell,
            executable=env.get(env.Vars.LAMBDA_LAYER_SHELL)
        )
    else:  # ...otherwise, there's a little less to do.
        proc = Popen(
            list(cmd),
            stdout=PIPE,
            stderr=PIPE
        )
    # Run the command and get the output.
    stdout, stderr = proc.communicate()

    # Create the process output object.
    output = ProcOutput(
        stdout=stdout.decode('utf-8'),
        stderr=stdout.decode('utf-8')
    )

    # Let's figure out how we're going to color our output.
    fg = None if proc.returncode == 0 else 'red'

    # If the failed, or if we're not running silent...
    if stdout and proc.returncode != 0 or not silent:
        # ...write out everything that happened.
        for line in stdout.decode('utf-8').split('\n'):
            click.echo(click.style(line, fg=fg))

    # If anything was printed to standard error, let's show that.
    if stderr:
        for line in stderr.decode('utf8').split('\n'):
            click.echo(click.style(line, fg='red'))

    # If the process failed...
    if proc.returncode != 0:
        # ...fail the whole application with the same code.
        sys.exit(proc.returncode)

    # Looks like we're all good here.
    return output


def _venv(
        path: Path,
        silent: bool = False
) -> Path:
    """
    Create a virtual environment.

    :param path: the path to the virtual environment
    :param silent: ``True`` to suppress normal output
    """
    # Set it up.
    cmd = [
        'python', '-m', 'venv',
        str(path)
    ]
    # Run it.
    _run(cmd, silent=silent)
    # Return the path to the caller.
    return path


def _requirements(
        path: Path,
        packages: Iterable[str],
        silent: bool = False
) -> Path:
    """
    Create a ``requirements.txt`` file.

    :param path: the output path
    :param packages: the packages
    :param silent: ``True`` to suppress normal output
    """
    # Figure out where we're going to write the files.
    _path = path.expanduser().resolve()
    # Write each package as a new line in the new requirements file.
    with open(str(_path), 'a') as fb:
        for package in packages:
            fb.write(f"{package}\n")
    # If we're not running silent...
    if not silent:
        # ...show 'em what we wrote.
        click.echo("requirements:")
        click.echo(_path.read_text())
    # Return the file path to the caller.
    return _path


def _install(
        venv: Path,
        requirements: Path,
        upgrade_pip: bool = True,
        silent: bool = False
):
    """
    Install requirements to a virtual environment.

    :param venv: the path to the virtual environment
    :param requirements: the path to a requirements file
    :param upgrade_pip:  ``True`` to upgrade ``pip`` before installing
        packages
    :param silent: ``True`` to suppress normal output
    """
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
    # Join up the commands so we can run them all-at-once.
    cmd = [' && '.join(cmds)]
    # Run it!
    _run(cmd, shell=True, silent=silent)


def _site_packages(venv: Path, silent: bool = False) -> Path:
    """
    Get the path to the ``site-packages`` directory for a virtual environment.

    :param venv: the path to the virtual environment
    :param silent: ``True`` to sppress normal output
    """
    # Put the commands together.  (Notice we need to run a shell command
    # that runs a couple of lines of python code... but we need to run it
    # in the context of the new virtual environment.)
    cmds = [
        f"source {venv}/bin/activate",
        'python -c "import site; print(site.getsitepackages())"'
    ]
    # Here we go.
    output = _run(
        cmd=[' && '.join(cmds)],
        shell=True,
        silent=silent
    )
    # Read the output and carve out the `site-packages` path.
    _path = Path(output.stdout[2:-3])
    # Return the path we found to the caller.
    return _path


def _archive(
        dir_path: Path,
        archive: Path
) -> Path:
    """
    Create an archive of a directory.

    :param dir_path: the directory to archive
    :param archive: the output archive path
    """
    # We'll need the length of the `site_packages` path so we can remove
    # it from the archive names of files we place into the .zip archive.
    site_packages_len = len(str(dir_path))
    # Let's start zippin'...
    with zipfile.ZipFile(str(archive), 'w', zipfile.ZIP_DEFLATED) as _zip:
        # ``_zip`` is zipfile handle.
        for root, dirs, files in os.walk(str(dir_path)):
            for file in files:
                path = os.path.join(root, file)
                arcname = "/python"+path[site_packages_len:]
                _zip.write(path, arcname=arcname)
    # Return the archive path to the caller.
    return archive


def make(
        dist_dir: Union[str, Path],
        layer: LayerConfig,
        silent: bool = False
) -> Path:
    """
    Make a layer.

    :param dist_dir: the path to the distribution directory
    :param layer: the layer configuration
    :param silent: ``True`` to suppress normal output
    """
    # Prepare the distribution directory.
    _dist_dir = (
        dist_dir if isinstance(dist_dir, Path) else Path(dist_dir)
    ).expanduser().resolve()
    # The distribution directory must be a directory.
    if _dist_dir.is_file():
        raise IsADirectoryError(f"{_dist_dir} is not a directory.")
    # Create the distribution directory if it doesn't exist.
    _dist_dir.mkdir(parents=True, exist_ok=True)

    # We're going to do this work in a temporary directory.
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Turn the `tmp_dir` string into a path.
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

        # Install the requirements.
        _install(venv=venv, requirements=requirements)

        # Get the path to the site packages directory.
        site_packages = _site_packages(venv=venv, silent=silent)

        # Create the archive.
        archive = _archive(
            # python=_python,
            dir_path=site_packages,
            archive=tmp_path / f"{layer.name}-{layer.version}.zip"
        )

        # Calculate the path to the final distribution archive.
        dist_path = _dist_dir / archive.name

        # If we're not running silent...
        if not silent:
            # ...let 'em know we're copying the file.
            click.echo(f"Copying  {archive} to {dist_path}")

        # Copy the archive to the distribution directory.
        shutil.copyfile(str(archive), str(dist_path))

        # Return the path to the distribution file.
        return dist_path
