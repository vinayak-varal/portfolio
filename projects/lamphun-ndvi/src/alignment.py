"""
Aligning two satellite scenes onto the same pixel grid.

Two downloads of the "same" area, taken at different times, are not
guaranteed to share an identical extent or resolution, a slightly
different zoom or pan in the source tool is enough to throw them out
of alignment. Pixel-by-pixel comparison (e.g. change detection) is
only meaningful once both images are resampled onto one common grid,
otherwise you're silently comparing unrelated ground locations.
"""

import numpy as np
from rasterio.warp import reproject, Resampling


def align_to_reference(source_array, source_transform, reference_shape,
                        reference_transform, crs="EPSG:4326"):
    """
    Resample a source array onto a reference image's exact grid.

    Parameters
    ----------
    source_array : ndarray
        The band data to be resampled (e.g. a second date's Red band).
    source_transform : affine.Affine
        The source array's affine transform (from rasterio's
        `.transform` on the opened file).
    reference_shape : tuple
        The (rows, cols) shape to resample onto, taken from whichever
        image is being treated as the fixed reference grid.
    reference_transform : affine.Affine
        The reference image's affine transform.
    crs : str
        Coordinate reference system shared by both images. Both
        downloads in this project used WGS84 (EPSG:4326).

    Returns
    -------
    ndarray
        The source data resampled onto the reference grid, same shape
        as reference_shape. Areas outside the source image's original
        coverage are filled with 0, which typically propagates to NaN
        once NDVI is computed (0/0), and downstream code should treat
        that as missing data, not a real measurement.
    """
    aligned = np.empty(reference_shape, dtype=np.float32)
    reproject(
        source=source_array,
        destination=aligned,
        src_transform=source_transform,
        src_crs=crs,
        dst_transform=reference_transform,
        dst_crs=crs,
        resampling=Resampling.bilinear,
    )
    return aligned
