"""
Subset a DestinE dataset.

This module extracts the requested variables, time range and
geographical region from a lazily opened xarray Dataset.
"""

from __future__ import annotations

import logging

import xarray as xr

from .config import BoundingBox

logger = logging.getLogger(__name__)


def subset(
    ds: xr.Dataset,
    *,
    variables: list[str],
    year: int,
    bbox: BoundingBox,
    level: int | None = None,
) -> xr.Dataset:
    """
    Return a spatial and temporal subset of a dataset.

    Parameters
    ----------
    ds
        Source dataset.

    variables
        Dataset variable names.

    year
        Calendar year to extract.

    bbox
        Geographic bounding box.

    level
        Pressure level to extract (hPa). Pass None for surface data.

    Returns
    -------
    xr.Dataset
        Lazy subset.
    """

    logger.info(
        "Subsetting year=%d variables=%s",
        year,
        ", ".join(variables),
    )

    #
    # Variable selection
    #

    ds = ds[variables]

    #
    # Pressure level selection
    #

    if level is not None:
        ds = ds.sel(isobaricInhPa=level)

    #
    # Time selection
    #

    time_dim = "valid_time" if "valid_time" in ds.dims else "time"

    ds = ds.sel(
        {time_dim: slice(
            f"{year}-01-01",
            f"{year}-12-31",
        )}
    )
    
    if ds.sizes[time_dim] == 0:
        raise ValueError(
            f"No data available for year {year}."
        )

    #
    # Latitude ordering
    #

    lat = ds.latitude

    if float(lat[0]) < float(lat[-1]):
        lat_slice = slice(
            bbox.south,
            bbox.north,
        )
    else:
        lat_slice = slice(
            bbox.north,
            bbox.south,
        )

    #
    # Spatial selection
    #

    ds = ds.sel(
        latitude=lat_slice,
        longitude=slice(
            bbox.west,
            bbox.east,
        ),
    )

    if ds.sizes["latitude"] == 0 or ds.sizes["longitude"] == 0:
        raise ValueError(
            "Bounding box does not intersect the dataset."
        )
    
    logger.info(
        "Subset dimensions: %s",
        dict(ds.sizes),
    )

    return ds
    
def subset_size(ds: xr.Dataset) -> str:
    """
    Return a compact description of the subset.
    """

    return (
        f"{len(ds.data_vars)} variables, "
        f"{ds.sizes['time']} timesteps, "
        f"{ds.sizes['latitude']}×{ds.sizes['longitude']} grid"
    )
