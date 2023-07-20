import numpy as np


def get_euclidean_distance_between_arrays(
    array_1: np.ndarray, array_2: np.ndarray
) -> np.ndarray:
    """
    Calculate the 2D Euclidean distance between corresponding points in two input arrays.

    The function computes the distance using only the x (0) and z (2) dimensions.

    Parameters:
    array_1 (np.ndarray): First input array with shape [X, 3], where X matches the other array.
    array_2 (np.ndarray): Second input array with shape [X, 3], where X matches the other array.

    Returns:
    np.ndarray: A 1D array of shape [X] containing the 2D Euclidean distances between corresponding points.
    """

    assert array_1.shape == array_2.shape, "Both input arrays must have the same shape"
    assert array_1.shape[1] == 3, "Each point must have 3 dimensions (x, y, z)"

    # Extract x and z dimensions from the arrays
    x1, z1 = array_1[:, 0], array_1[:, 2]
    x2, z2 = array_2[:, 0], array_2[:, 2]

    # Compute the 2D difference and squared difference
    squared_diff_x = (x1 - x2) ** 2
    squared_diff_z = (z1 - z2) ** 2

    # Compute the sum of squared differences and the final distances
    sum_squared_diff = squared_diff_x + squared_diff_z
    distances = np.sqrt(sum_squared_diff)

    return distances
