"""
Configuration handling for the DestinE downloader.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Dataset(BaseModel):
    name: str | None = None
    url: str


class DatasetConfig(BaseModel):
    surface: Dataset
    pressure: Dataset


class BoundingBox(BaseModel):
    """Bounding box in geographic coordinates."""

    west: float
    east: float
    south: float
    north: float

    @model_validator(mode="after")
    def validate_bbox(self):
        if self.east <= self.west:
            raise ValueError("east must be greater than west")

        if self.north <= self.south:
            raise ValueError("north must be greater than south")

        if not (-180 <= self.west <= 180):
            raise ValueError("west longitude must be between -180 and 180")

        if not (-180 <= self.east <= 180):
            raise ValueError("east longitude must be between -180 and 180")

        if not (-90 <= self.south <= 90):
            raise ValueError("south latitude must be between -90 and 90")

        if not (-90 <= self.north <= 90):
            raise ValueError("north latitude must be between -90 and 90")

        return self


class YearRange(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def validate_years(self):
        if self.end < self.start:
            raise ValueError("end year must be >= start year")
        return self


class PressureConfig(BaseModel):
    variables: list[str]
    levels: list[int]

    @model_validator(mode="after")
    def validate_levels(self):
        if len(self.levels) == 0:
            raise ValueError("At least one pressure level is required")

        if any(level <= 0 for level in self.levels):
            raise ValueError("Pressure levels must be positive")

        return self


class Config(BaseModel):

    model_config = ConfigDict(extra="forbid")

    version: Annotated[int, Field(default=1)]

    datasets: DatasetConfig

    bbox: BoundingBox

    years: YearRange

    surface: list[str]

    pressure: PressureConfig

    output: Path


def load_config(filename: str | Path) -> Config:
    """
    Load a YAML configuration file.
    """

    filename = Path(filename)

    with filename.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    cfg = Config.model_validate(data)

    cfg.output.mkdir(
        parents=True,
        exist_ok=True,
    )

    return cfg
