"""
Open DestinE Climate DT datasets.
"""

from __future__ import annotations
import logging
import xarray as xr
from os import PathLike

logger = logging.getLogger(__name__)


def open_dataset(
    url: str | PathLike[str],
    *,
    zarr_format: int | None = None,
) -> xr.Dataset:
    """
    Open a remote DestinE Climate DT Zarr dataset.

    Parameters
    ----------
    url
        URL of the remote Zarr store.

    zarr_format
        Zarr format version. Use 3 for Climate DT Gen2 datasets,
        None for auto-detection (ERA5).

    Returns
    -------
    xarray.Dataset
        Lazily opened dataset backed by Dask arrays.

    Notes
    -----
    The Climate DT Generation 2 datasets use Zarr v3 and require
    authenticated HTTP access. Authentication is handled via the
    user's ~/.netrc file by enabling ``trust_env=True``.
    """

    logger.info("Opening dataset")
    logger.info("URL: %s", url)

    kwargs: dict = {
        "engine": "zarr",
        "zarr_format": 3,
        "chunks": {},          # Preserve native chunking
        "storage_options": {
            "client_kwargs": {
                "trust_env": True,
            }
        },
    }

    if zarr_format is not None:
        kwargs["zarr_format"] = zarr_format

    ds = xr.open_dataset(url, **kwargs)

    logger.info(
        "Opened dataset with %d variables",
        len(ds.data_vars),
    )

    return ds
    
    def list_variables(ds: xr.Dataset) -> list[str]:
        """
        Return dataset variables sorted alphabetically.
        """

        return sorted(ds.data_vars)
        
    def dataset_summary(ds: xr.Dataset) -> str:
        """
        Return a concise summary of a dataset.
        """
        
        return (
            f"{len(ds.data_vars)} variables, "
            f"{len(ds.time)} timesteps"
        )
