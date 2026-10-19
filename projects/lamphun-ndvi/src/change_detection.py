"""
Converting pixel counts into real-world hectares, and comparing two
classified dates to detect vegetation loss.
"""

import numpy as np


def pixel_area_hectares(transform):
    """
    Compute the real-world ground area of one pixel, in hectares.

    Pixel size in a WGS84 (geographic) GeoTIFF is stored in degrees,
    not meters, and degrees are not a fixed physical distance: a
    degree of longitude shrinks the further you are from the equator,
    while a degree of latitude is roughly constant everywhere. Both
    conversions are needed before pixel counts mean anything in real
    units.

    Parameters
    ----------
    transform : affine.Affine
        The image's affine transform (from rasterio's `.transform`).
        `.a` is pixel width in degrees longitude, `.e` is pixel height
        in degrees latitude (negative, since row index increases
        downward while latitude decreases), and `.f` is the latitude
        of the image's top-left corner, used here as a reasonable
        approximation of the scene's latitude for the conversion.

    Returns
    -------
    float
        Ground area of one pixel, in hectares.
    """
    meters_per_degree_lat = 111_320
    height_m = np.abs(transform.e) * meters_per_degree_lat
    width_m = transform.a * np.cos(np.radians(transform.f)) * meters_per_degree_lat
    area_m2 = height_m * width_m
    return area_m2 / 10_000


def area_by_class(classified, pixel_area_ha):
    """
    Total hectares in each class of a classified array.

    Returns
    -------
    dict
        {"vegetation": float, "non_vegetation": float}, in hectares.
        NaN pixels (missing data) are automatically excluded, since
        neither `== 1` nor `== 0` is True for NaN.
    """
    return {
        "vegetation": np.sum(classified == 1) * pixel_area_ha,
        "non_vegetation": np.sum(classified == 0) * pixel_area_ha,
    }


def vegetation_loss(classified_before, classified_after, pixel_area_ha):
    """
    Detect pixels that were vegetation in an earlier scene and are not
    in a later one, and convert the count to hectares.

    Both arrays must already be aligned to the same grid (see
    alignment.align_to_reference) and classified with a consistent
    threshold, ideally the same threshold, or two independently
    derived thresholds that were confirmed to closely agree (see
    threshold.find_threshold).

    A critical, easy-to-get-backwards detail: confirm which array is
    actually the earlier date and which is the later date from the
    source filenames before calling this, not from memory. Swapping
    them silently turns "vegetation lost" into "vegetation gained"
    with no error thrown.

    Parameters
    ----------
    classified_before : ndarray
        Classification from the earlier date.
    classified_after : ndarray
        Classification from the later date, same shape, same grid.
    pixel_area_ha : float
        Ground area of one pixel, in hectares (see pixel_area_hectares).

    Returns
    -------
    tuple
        (change_mask, hectares_converted). change_mask is a boolean
        array, True where a pixel was vegetation and is now not.
    """
    was_vegetation = classified_before == 1
    is_now_nonveg = classified_after == 0
    change_mask = was_vegetation & is_now_nonveg
    hectares_converted = np.sum(change_mask) * pixel_area_ha
    return change_mask, hectares_converted
