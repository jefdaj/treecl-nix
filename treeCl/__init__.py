from __future__ import absolute_import

# quiet down matplotlib
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

from .alignment import Alignment
from .clustering import Spectral, Hierarchical, MultidimensionalScaling, Automatic, Evaluation
from .collection import Collection, Scorer
from .concatenation import Concatenation
from .distance_matrix import CoordinateMatrix, DistanceMatrix
from .partition import Partition
from .plotter import Plotter
from .simulator import Simulator
from .tree import Tree

import logging.config
import yaml
from pkg_resources import resource_string
conf = resource_string(__name__, 'logging/logging.yaml')

# full_load fixes a security warning:
# https://www.discoverbits.in/892/yamlloadwarning-calling-yaml-load-without-loader-deprecated
D = yaml.full_load(conf)
D.setdefault('version', 1)
logging.config.dictConfig(D)
del D
