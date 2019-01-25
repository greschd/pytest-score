# -*- coding: utf-8 -*-

# © 2015-2018, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines a pytest plugin for tests which have a 'score' in addition to a binary pass / fail result.
"""

__version__ = '0.0.0a1'

from ._fixtures import *
from ._plugin import *
