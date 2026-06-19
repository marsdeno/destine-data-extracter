"""
Download task generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import Config


@dataclass(frozen=True, slots=True)
class DownloadTask:
    """
    Represents a single download.

    One task corresponds to one variable for one year,
    optionally at a specific pressure level.
    """
    
    dataset: str
    variable: str
    year: int
    level: int | None = None

    def output_file(
        self,
        output_root: Path,
    ) -> Path:
        """
        Return the NetCDF filename for this task.

        Examples
        --------
        output/
            surface/
                t2m/
                    2035.nc

        output/
            pressure/
                t/
                    850/
                        2035.nc
        """

        path = output_root / self.dataset / self.variable

        if self.level is not None:
            path = path / str(self.level)

        return path / f"{self.year}.nc"

    def __str__(self) -> str:
        """Human-readable task description."""

        return f"{self.variable} ({self.year})"


def build_surface_tasks(
    cfg: Config,
    variables: list[str],
) -> list[DownloadTask]:
    """
    Build the list of surface download tasks.
    """

    tasks: list[DownloadTask] = []

    for year in cfg.years.years:
        for variable in variables:
            tasks.append(
                DownloadTask(
                    dataset="surface",
                    variable=variable,
                    year=year,
                )
            )

    return tasks


def build_pressure_tasks(
    cfg: Config,
    variables: list[str],
) -> list[DownloadTask]:
    """
    Build the list of pressure-level download tasks.
    """

    if cfg.pressure is None:
        return []

    tasks: list[DownloadTask] = []

    for year in cfg.years.years:
        for variable in variables:
            for level in cfg.pressure.levels:
                tasks.append(
                    DownloadTask(
                        dataset="pressure",
                        variable=variable,
                        year=year,
                        level=level,
                    )
                )

    return tasks
