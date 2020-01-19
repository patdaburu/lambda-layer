#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from lambda_layer import config
import pytest
from lambda_layer.config import LayerConfig


def config_path(name: str) -> Path:
    return Path(__file__).parent / 'data' / name



def test_loadf_single():
    configs = list(LayerConfig.loadf(config_path('lambda-layer.toml')))

    print()
    for config in configs:
        print(config)

