"""Functions to convert interface types into data types used by joint_model """
import numpy as np

from ..interfaces import *
from . import geometry as geom

class Converter:

    @property
    def types(self):
        return {
            Nodes: geom.nodes_to_dataframe,
            Elements: geom.elements_to_dataframe
        }