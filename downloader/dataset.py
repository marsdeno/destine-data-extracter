"""
Open Destination Earth Climate DT datasets.
"""

from __future__ import annotations

import logging

import xarray as xr

logger = logging.getLogger(__name__)


def open_dataset(url: str) -> xr.Dataset:
    """
    Open a remote Zarr dataset.

    Parameters
    ----------
    url
        URL of the remote Zarr store.

    Returns
    -------
    xarray.Dataset
    """

    logger.info("Opening dataset")
    logger.info(url)

    ds = xr.open_dataset(
        url,
        engine="zarr",
        zarr_format=3,
        chunks={},               # Preserve native chunking
        storage_options={
            "client_kwargs": {
                "trust_env": True,
            }
        },
    )

    logger.info("Dataset opened successfully")

    return ds
