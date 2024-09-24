import numpy as np

def get_matrix_from_dict(d):
    """
    Returns a 4x4 matrix given a dictionary with 16 values
    """
    coefficients = np.array(list(d.values()))
    return coefficients.reshape((4, 4))