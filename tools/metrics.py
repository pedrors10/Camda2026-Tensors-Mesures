import numpy as np


def chi2_distance(p, q):

    mask = (p + q) > 0

    return np.sum(
        (p[mask] - q[mask])**2 /
        (p[mask] + q[mask])
    )
