"""
Download DestinE Climate DT data.

This is the main entry point for the downloader.
"""

from __future__ import annotations

import logging
import time

from downloader.config import load_config
from downloader.dataset import open_dataset
from downloader.retry import retry
from downloader.subset import subset
from downloader.tasks import (
    DownloadTask,
    build_pressure_tasks,
    build_surface_tasks,
)
from downloader.variables import (
    PRESSURE_VARIABLES,
    SURFACE_VARIABLES,
    translate,
)
from downloader.writer import write_netcdf


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


def process_tasks(
    tasks: list[DownloadTask],
    ds,
    cfg,
    failures: list[str],
) -> None:

    for i, task in enumerate(tasks, start=1):

        outfile = task.output_file(cfg.output)

        if outfile.exists():

            logger.info(
                "[%d/%d] Skipping %s",
                i,
                len(tasks),
                outfile.name,
            )

            continue

        logger.info(
            "[%d/%d] %s",
            i,
            len(tasks),
            task,
        )

        regional = subset(
            ds,
            variables=[task.variable],
            year=task.year,
            bbox=cfg.bbox,
            level=task.level,
        )

        try:

            retry(
                lambda: write_netcdf(
                    regional,
                    outfile,
                ),
                retries=cfg.download.retries,
                delay=cfg.download.retry_delay,
            )

        except Exception:

            logger.exception(
                "Failed: %s",
                task,
            )

            failures.append(str(task))


def main() -> None:

    start = time.perf_counter()

    #
    # Configuration
    #

    cfg = load_config("config.yaml")

    surface_variables = translate(
        cfg.surface.variables,
        SURFACE_VARIABLES,
    )

    pressure_variables: list[str] = []

    if cfg.pressure is not None:
        pressure_variables = translate(
            cfg.pressure.variables,
            PRESSURE_VARIABLES,
        )

    surface_tasks = build_surface_tasks(
        cfg,
        surface_variables,
    )

    pressure_tasks = build_pressure_tasks(
        cfg,
        pressure_variables,
    )

    total_tasks = len(surface_tasks) + len(pressure_tasks)

    logger.info("Configuration")
    logger.info("-------------")
    logger.info("Variables    : %d surface, %d pressure",
                 len(surface_variables), len(pressure_variables))
    logger.info(
        "Years        : %d-%d",
        cfg.years.start,
        cfg.years.end,
    )
    if cfg.pressure is not None:
        logger.info("Pressure lvl : %s", cfg.pressure.levels)
    logger.info("Tasks        : %d (%d surface, %d pressure)",
                 total_tasks, len(surface_tasks), len(pressure_tasks))
    logger.info("Output       : %s", cfg.output)
    logger.info("")

    failures: list[str] = []

    #
    # Surface download
    #

    if surface_tasks:

        logger.info("Surface downloads")
        logger.info("-----------------")

        ds_surface = open_dataset(
            cfg.datasets.surface.url,
            zarr_format=3,
        )

        process_tasks(surface_tasks, ds_surface, cfg, failures)

    #
    # Pressure-level download
    #

    if pressure_tasks:

        logger.info("Pressure-level downloads")
        logger.info("------------------------")

        ds_pressure = open_dataset(
            cfg.datasets.pressure.url,
        )

        process_tasks(pressure_tasks, ds_pressure, cfg, failures)

    elapsed = time.perf_counter() - start

    logger.info("")
    logger.info("Completed")
    logger.info("---------")
    logger.info("Elapsed : %.1f minutes", elapsed / 60)
    logger.info("Failed  : %d", len(failures))

    if failures:

        logger.info("")

        for task in failures:
            logger.info("  %s", task)


if __name__ == "__main__":
    main()
