"""
dataset.py

Open a Generation 2 Climate DT Zarr dataset.
"""

from __future__ import annotations

import logging

import xarray as xr

logger = logging.getLogger(__name__)


class ClimateDataset:

    def __init__(self, url: str):

        self.url = url
        self._ds = None

    @property
    def ds(self) -> xr.Dataset:

        if self._ds is None:
            self.open()

        return self._ds

    def open(self):

        logger.info("Opening dataset")

        logger.info(self.url)

        self._ds = xr.open_dataset(
            self.url,
            engine="zarr",
            zarr_format=3,
            chunks="auto",
            storage_options={
                "client_kwargs": {
                    "trust_env": True,
                }
            },
        )

        logger.info("Dataset opened")

        return self._ds

    @property
    def variables(self):

        return sorted(self.ds.data_vars)

    @property
    def coordinates(self):

        return sorted(self.ds.coords)

    def summary(self):

        print()

        print("=" * 60)

        print("Variables")

        print("-" * 60)

        for variable in self.variables:

            print(variable)

        print()

        print("=" * 60)

        print("Coordinates")

        print("-" * 60)

        for coordinate in self.coordinates:

            print(coordinate)

        print()

        print(self.ds)
