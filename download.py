#!/usr/bin/env python3

"""
Download a regional subset of the DestinE Climate DT surface dataset.
"""

from __future__ import annotations

import logging
from pathlib import Path

from downloader.config import load_config
from downloader.dataset import open_dataset
from downloader.subset import subset
from downloader.variables import translate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


def main():

    cfg = load_config("config.yaml")

    logger.info("Opening surface dataset")

    ds = open_dataset(
        cfg.datasets.surface.url
    )

    variables = translate(
        cfg.surface
    )

    logger.info(
        "Variables: %s",
        variables,
    )

    year = cfg.years.start

    regional = subset(
        ds,
        variables=variables,
        bbox=cfg.bbox,
        year=year,
    )

    logger.info(regional)

    output_dir = Path(cfg.output) / "surface"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    outfile = (
        output_dir
        / f"{variables[0]}_{year}.nc"
    )

    logger.info(
        "Writing %s",
        outfile,
    )

    regional.to_netcdf(
        outfile
    )

    logger.info("Finished")


if __name__ == "__main__":
    main()
