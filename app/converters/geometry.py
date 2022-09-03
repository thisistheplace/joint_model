import pandas as pd

from ..interfaces import *

def nodes_to_dataframe(nodes: Nodes) -> pd.DataFrame:
    """Converts Nodes to pandas DataFrame
    
    Args:
        nodes (Nodes): object

    Returns Dataframe of x, y, z coordinates (3, len), index by node id
    """
    return pd.DataFrame(
        ({
            "name": node.name,
            "id": node.id,
            "x": node.coordinate.x,
            "y": node.coordinate.y,
            "z": node.coordinate.z
        } for node in nodes.nodes)
    )

def elements_to_dataframe(elements: Elements) -> pd.DataFrame:
    """Converts Elements to pandas DataFrame
    
    Args:
        nodes (Elements): object

    Returns Dataframe of connected node ids, indexed by element id
    """
    return pd.DataFrame(elements.elements)