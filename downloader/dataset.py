from __future__ import annotations

import logging

import xarray as xr

logger = logging.getLogger(__name__)


class ClimateDataset:

    def __init__(self, url: str):

        self.url = url
        self._ds = None

    @property
    def ds(self):

        if self._ds is None:
            self.open()

        return self._ds

    def open(self):

        logger.info("Opening")

        logger.info(self.url)

        self._ds = xr.open_dataset(
            self.url,
            engine="zarr",
            zarr_format=3,
            chunks={},
            storage_options={
                "client_kwargs": {
                    "trust_env": True,
                }
            },
        )

        logger.info("Opened successfully")

        return self._ds
