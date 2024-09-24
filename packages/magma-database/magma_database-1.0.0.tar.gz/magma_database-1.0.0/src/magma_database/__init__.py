#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .config import config
from .database import Volcano, Station, Sds
from pkg_resources import get_distribution

__version__ = get_distribution("magma-database").version
__author__ = "Martanto"
__author_email__ = "martanto@live.COM"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024, MAGMA Indonesia"
__url__ = "https://github.com/martanto/magma-database"

__all__ = [
    "Volcano",
    "Station",
    "Sds",
    "config",
]