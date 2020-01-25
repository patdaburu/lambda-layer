#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 1/19/20
"""
Environment variables.

.. currentmodule:: lambda_layer.env
.. moduleauthor:: Pat Daburu <pat@daburu.net>
"""
import os
from pathlib import Path
from enum import Enum
from typing import NamedTuple, Union


class Vars(Enum):
    """Well-known environment variables."""

    #: the layer configuration path
    LAMBDA_LAYER_CONFIG = 'LAMBDA_LAYER_CONFIG'
    #: the distribution directory
    LAMBDA_LAYER_DIST_DIR = 'LAMBDA_LAYER_DIST_DIR'
    #: the path to the shell executable
    LAMBDA_LAYER_SHELL = 'LAMBDA_LAYER_SHELL'


class VarDef(NamedTuple):
    """Defines an environment variable."""

    default: str  #: the default value
    help: str  #: the help string


_VARS = {
    Vars.LAMBDA_LAYER_CONFIG:  VarDef(
        default=str(Path.cwd().expanduser().resolve() / '.lambda-layer.toml'),
        help='path to the layer configuration'
    ),
    Vars.LAMBDA_LAYER_DIST_DIR:  VarDef(
        default=str(Path.cwd().expanduser().resolve() / 'aws-dist'),
        help='path to the distribution directory'
    ),
    Vars.LAMBDA_LAYER_SHELL: VarDef(
        default='/bin/bash',
        help='path to the shell executable'
    )
}  #: environment variable definitions


def get(var: Vars) -> Union[str, None]:
    """Get the value of an environment variable."""
    if var.name in os.environ:
        return os.environ.get(var.name)
    var_def = _VARS.get(var)
    if var_def:
        return var_def.default
    return None
