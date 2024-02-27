import os

import numpy as np



def multiply_mats(*mats: np.ndarray):
    operation = lambda M1, M2 : np.matmul(M1, M2)
    if len(mats) < 2:
        raise Exception("Not enough matrices")
    if len(mats) == 2:
        return operation(mats[0], mats[1])
    return operation(mats[0], multiply_mats(*mats[1:]))


def find_available_cores() -> int:
    """
    Returns the number of available CPU cores on the current system.

    Returns:
        int: The number of available CPU cores.
    """
    return os.cpu_count()