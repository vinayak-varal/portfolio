# Vegetation Loss in the Lamphun Industrial Corridor

A from-scratch NDVI pipeline on real Sentinel-2 imagery over Lamphun,
Thailand, built to detect vegetation converted to non-vegetation (a
proxy for industrial/warehouse development) between January 2024 and
January 2026.

**Full write-up with figures:** see the project page on
[the portfolio site](../../index.html), or `index.html` in this folder.

## Results

| Metric | Value |
|---|---|
| NDVI threshold (derived, not assumed) | ≈ 0.06 |
| Vegetation cover, Jan 2026 | 94.4% of scene |
| Total scene area | ~97,258 ha (~972 km²) |
| Vegetation lost, Jan 2024 → Jan 2026 | **863 ha** |

## What this project actually demonstrates

- NDVI derived from first principles (band physics, not a library call)
- A nodata artifact found and masked *before* it could bias results
  (~0.07% of pixels, flagged via a suspicious spike at exactly -1.0)
- A classification threshold derived from the scene's own histogram
  (a manual valley-finding approach, conceptually related to Otsu's
  method), rather than an assumed round number
- Ground-truthing a classified pixel cluster against real satellite
  maps, and correctly attributing an ambiguous result to a mixed-pixel
  effect rather than overclaiming
- Reprojecting and aligning two independently-downloaded scenes with
  different extents and resolutions onto a common grid before
  comparing them
- **Catching a seasonal confound**: an initial May-2024-vs-June-2026
  comparison found an implausible 4,431 ha of "change," which turned
  out to be mostly the wet/dry season transition, not real land-use
  change. Re-running with matched months (Jan vs Jan) corrected this
  to 863 ha.

## Data

Sentinel-2 L2A imagery, bands B04 (Red) and B08 (NIR), downloaded from
the [Copernicus Data Space Ecosystem](https://browser.dataspace.copernicus.eu/)
as raw GeoTIFF (32-bit float, WGS84), not a pre-rendered visualization.

Raw `.tif` files are not committed to this repository (see
`.gitignore`); download your own via Copernicus Browser using the same
band/format settings to reproduce.

## Structure

```
src/
  ndvi.py              NDVI computation + nodata masking
  threshold.py         Histogram valley-finding for classification threshold
  classify.py          NDVI -> vegetation/non-vegetation classification
  alignment.py         Reprojecting a second date onto a reference grid
  change_detection.py  Area statistics + before/after change detection
```

## Known limitations

- Downloaded at resampled ~18m resolution, not Sentinel-2's native 10m
- WGS84 geographic coordinates, not a projected CRS (handled via a
  latitude-aware degrees-to-meters conversion, see
  `change_detection.pixel_area_hectares`)
- No dedicated cloud masking; low cloud-cover filtering was applied at
  download time but cloud contamination is not separately excluded
- NDVI alone cannot cleanly separate water, bare soil, and built-up
  land at boundaries or in mixed pixels

## Requirements

```
pip install -r requirements.txt
```
