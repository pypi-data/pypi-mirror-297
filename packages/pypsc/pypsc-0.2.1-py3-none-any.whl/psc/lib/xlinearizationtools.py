import numpy as np
import math

def radius_from_volume(dim: int, volume: float) -> float:
    """returns radius of N-dimensional sphere

    Args:
        dim (int): dimension of PS
        volume (float): volume of polytope in PS

    Returns:
        float: returns radius of N-dimensional sphere
    """    
    # Calculate radius of sphere in 'dimension'al space from its volume
    R = ((volume * math.gamma((dim / 2) + 1)) / (math.pi ** (dim / 2))) ** (1 / dim)
    return R