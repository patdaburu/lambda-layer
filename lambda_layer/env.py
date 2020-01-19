#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 1/19/20
"""
Environment variables.

.. currentmodule:: env
.. moduleauthor:: Pat Daburu <pat@daburu.net>
"""
import os
from pathlib import Path
from enum import Enum
from typing import NamedTuple, Union


class Vars(Enum):
    #: the distribution directory
    LAMBDA_LAYER_DIST_DIR: 'LAMBDA_LAYER_DIST_DIR'


class VarDef(NamedTuple):
    default: str
    help: str


_VARS = {
    Vars.LAMBDA_LAYER_DIST_DIR:  VarDef(
        default=str(Path.cwd().expanduser().resolve() / '.lambda-layer.toml'),
        help='The path to the layer configuration file.'
    )
}


def get(var: Vars) -> Union[str, None]:
    if var.name in os.environ:
        return os.environ.get(var.name)
    var_def = _VARS.get(var)
    if var_def:
        return var_def.default
    return None

