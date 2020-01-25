#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 1/19/20
"""
Configuration objects.

.. currentmodule:: lambda_layer.config
.. moduleauthor:: Pat Daburu <pat@daburu.net>
"""
from pathlib import Path
from typing import Any, Mapping, NamedTuple, Tuple, Union
import toml


class LayerConfig(NamedTuple):
    """A layer configuration."""
    name: str  #: the name of the layer
    version: str  #: the layer version
    packages: Tuple[str]  #: the installed packages

    @classmethod
    def load(cls, data: Mapping[str, Any]) -> 'LayerConfig':
        return LayerConfig(**{
            **data,
            'packages': tuple(data.get('packages', []))
        })


class Config(NamedTuple):
    environment: Mapping[str, str]
    layers: Tuple[LayerConfig]

    @classmethod
    def load(cls, data: Mapping[str, Any]) -> 'Config':
        return Config(**{
            'environment': dict(data.get('environment', {})),
            'layers': tuple([
                LayerConfig.load(layer) for layer in data.get('layers', [])
            ])
        })

    @classmethod
    def loadf(
            cls,
            path: Union[str, Path]
    ) -> 'Config':
        _path = (
            path if isinstance(path, Path) else Path(path)
        ).expanduser().resolve()
        # If the file doesn't exist, there isn't much more we can do here.
        if not _path.exists():
            raise FileNotFoundError(_path)
        elif _path.is_dir():
            raise IsADirectoryError(_path)

        # Read the contents.
        data = toml.loads(_path.read_text())

        # Parse it out.
        return cls.load(data)


