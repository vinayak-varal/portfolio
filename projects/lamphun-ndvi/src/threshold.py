"""
Deriving a vegetation/non-vegetation threshold from the data itself,
rather than assuming a round number like 0.2 from a textbook.

The approach: water, soil, and built-up pixels cluster at one region
of the NDVI histogram; vegetation clusters at another. The point where
pixel counts dip to a local minimum between the two populations is the
least ambiguous place to draw a dividing line, this is the same idea
behind Otsu's method for image thresholding, applied here by directly
inspecting the histogram rather than importing a library implementation.
"""

import numpy as np


def find_threshold(ndvi_array, search_min=-0.1, search_max=0.3, bins=100):
    """
    Find the local minimum ("valley") in an NDVI histogram within a
    given search window.

    The search window itself is a judgment call, based on where the
    vegetation/non-vegetation transition visually appears to sit in a
    first look at the histogram. Narrow it or widen it if a new scene's
    histogram looks meaningfully different from the one this project
    was built against.

    Parameters
    ----------
    ndvi_array : ndarray
        NDVI values, with nodata already masked to NaN (see
        ndvi.mask_nodata). NaNs are dropped before histogramming.
    search_min, search_max : float
        The NDVI range to search for a valley within.
    bins : int
        Number of histogram bins across the full [-1, 1] range.

    Returns
    -------
    float or None
        The NDVI value at the valley, or None if no local minimum was
        found in the search window (worth handling explicitly rather
        than silently falling back to a default).
    """
    valid = ndvi_array[~np.isnan(ndvi_array)]
    counts, bin_edges = np.histogram(valid, bins=bins, range=(-1, 1))

    mask = (bin_edges[:-1] >= search_min) & (bin_edges[:-1] <= search_max)
    region_counts = counts[mask]
    region_edges = bin_edges[:-1][mask]

    for i in range(len(region_counts)):
        left = region_counts[max(i - 1, 0)]
        right = region_counts[min(i + 1, len(region_counts) - 1)]
        if region_counts[i] < left and region_counts[i] < right:
            return region_edges[i]

    return None
