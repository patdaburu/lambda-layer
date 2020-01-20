#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 1/19/20
"""
Create AWS lambda layer packages.

.. currentmodule:: lambda_layer.package
.. moduleauthor:: Pat Daburu <pat@daburu.net>
"""
from pathlib import Path
from typing import Union
from lambda_layer.config import LayerConfig
from . import bash


def make(
        # python: str,
        dist_dir: Union[str, Path],
        layer: LayerConfig,
        silent: bool = False
) -> Path:
    # TODO: Create options for Windows.
    return bash.make(
        # python=python,
        dist_dir=dist_dir,
        layer=layer,
        silent=silent
    )
