"""
Turning continuous NDVI values into a discrete vegetation /
non-vegetation classification.
"""

import numpy as np


def classify(ndvi_array, threshold):
    """
    Classify NDVI pixels as vegetation (1) or non-vegetation (0).

    NaN pixels (nodata, or areas outside a reprojected image's
    coverage) are explicitly preserved as NaN rather than being
    silently swept into one class or the other. This matters: NaN
    compared with >= always evaluates to False in numpy, so without
    this explicit check, every nodata pixel would quietly be counted
    as "non-vegetation," corrupting downstream area statistics with
    no error or warning.

    Parameters
    ----------
    ndvi_array : ndarray
        NDVI values, nodata already masked to NaN.
    threshold : float
        NDVI value at or above which a pixel is classified as
        vegetation. See threshold.find_threshold for how this is
        derived from the data rather than assumed.

    Returns
    -------
    ndarray
        Same shape as input. 1 = vegetation, 0 = non-vegetation,
        NaN = missing data (preserved from the input).
    """
    return np.where(
        np.isnan(ndvi_array),
        np.nan,
        np.where(ndvi_array >= threshold, 1, 0),
    )
