"""
Subsetting utilities.
"""

from __future__ import annotations

import xarray as xr

from .config import BoundingBox


def subset(
    ds: xr.Dataset,
    *,
    variables: list[str],
    bbox: BoundingBox,
    year: int,
) -> xr.Dataset:
    """
    Spatially and temporally subset a Climate DT dataset.
    """

    return (
        ds[variables]
        .sel(
            longitude=slice(
                bbox.west,
                bbox.east,
            ),
            latitude=slice(
                bbox.south,
                bbox.north,
            ),
            time=slice(
                f"{year}-01-01",
                f"{year}-12-31T23:59:59",
            ),
        )
    )
