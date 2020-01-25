#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 1/19/20
"""
Create AWS lambda layer packages.

.. currentmodule:: lambda_layer.package
.. moduleauthor:: Pat Daburu <pat@daburu.net>
"""
from pathlib import Path
import platform
from typing import Union
from lambda_layer.config import LayerConfig
from . import bash


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
    if platform.system() == 'Windows':
        raise NotImplementedError("Windows isn't supported just yet.")

    return bash.make(
        dist_dir=dist_dir,
        layer=layer,
        silent=silent
    )
