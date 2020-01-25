#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 1/25/20
"""
Objects and functions common to all environments.

.. currentmodule:: lambda_layer.package.common
.. moduleauthor:: Pat Daburu <pat@daburu.net>
"""
from typing import NamedTuple


class ProcOutput(NamedTuple):
    """Output from external processes."""

    stdout: str  #: standard out (STDOUT)
    stderr: str  #: standard error (STDERR)
