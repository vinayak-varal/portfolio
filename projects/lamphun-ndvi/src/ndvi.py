"""
NDVI computation.

NDVI (Normalized Difference Vegetation Index) exploits a simple fact
about plant physiology: chlorophyll absorbs red light for photosynthesis
but reflects near-infrared (NIR) light strongly, since it has no use
for it. Water absorbs both. Bare soil and built-up surfaces sit
somewhere in between. NDVI turns that relationship into a single
number between -1 and 1.
"""

import numpy as np


def compute_ndvi(nir, red):
    """
    Compute NDVI from NIR and Red reflectance arrays (or scalars).

    Works elementwise on numpy arrays of any shape, a single formula
    applies whether you're looking at one pixel or a 10,000 x 10,000
    satellite scene, with no changes needed.

    Parameters
    ----------
    nir : array_like
        Near-infrared band reflectance (e.g. Sentinel-2 B08).
    red : array_like
        Red band reflectance (e.g. Sentinel-2 B04).

    Returns
    -------
    ndarray
        NDVI values in [-1, 1]. Water and built-up surfaces tend to be
        low or negative; healthy vegetation tends to be high (often
        0.5-0.9 in a wet-season scene).
    """
    nir = np.asarray(nir, dtype=float)
    red = np.asarray(red, dtype=float)
    return (nir - red) / (nir + red)


def mask_nodata(ndvi_array, threshold=-0.99):
    """
    Flag and mask suspected nodata artifacts.

    Real reflectance data essentially never produces a value sitting
    exactly at a round number like -1.0 across a meaningful cluster of
    pixels. A spike there is a strong signal of nodata (tile edges,
    reprojection gaps) rather than real measurements, and should be
    excluded before any statistics are computed on the array.

    Always check what fraction of the image this affects before
    trusting the mask, a small artifact (a fraction of a percent) is
    expected; anything large suggests a different problem.

    Parameters
    ----------
    ndvi_array : ndarray
        Raw NDVI values, possibly containing nodata artifacts.
    threshold : float
        Values at or below this are treated as nodata. Default -0.99
        was chosen by inspecting this project's own histogram, not a
        universal constant, re-derive it for new data sources.

    Returns
    -------
    ndarray
        Same shape as input, with suspected nodata pixels set to NaN.
    """
    suspicious = ndvi_array <= threshold
    fraction = suspicious.mean()
    if fraction > 0.02:
        print(f"Warning: {fraction:.2%} of pixels flagged as nodata, "
              f"this is unusually high, verify before trusting the mask.")
    return np.where(suspicious, np.nan, ndvi_array)
