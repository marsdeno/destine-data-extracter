"""
Configuration handling.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class Dataset(BaseModel):
    url: str


class Datasets(BaseModel):
    surface: Dataset
    pressure: Dataset | None = None


class BoundingBox(BaseModel):
    west: float
    east: float
    south: float
    north: float
    
#    @model_validator(mode="after")
#    def validate(self):
#
#        if self.west >= self.east:
#            raise ValueError("west must be less than east")
#
#        if self.south >= self.north:
#            raise ValueError("south must be less than north")
#
#        return self

class Years(BaseModel):
    start: int
    end: int

    @property
    def years(self) -> range:
        return range(self.start, self.end + 1)

#    @model_validator(mode="after")
#    def validate(self):
#
#        if self.end < self.start:
#            raise ValueError("end year must not precede start year")
#
#        return self

class VariableSelection(BaseModel):
    variables: list[str]


class PressureSelection(VariableSelection):
    levels: list[int] = Field(default_factory=list)


class DownloadOptions(BaseModel):
    retries: int = 3
    retry_delay: int = 10


class Config(BaseModel):
    datasets: Datasets

    bbox: BoundingBox

    years: Years

    surface: VariableSelection

    pressure: PressureSelection | None = None

    output: Path

    download: DownloadOptions


def load_config(filename: str | Path) -> Config:

    with open(filename) as f:
        data = yaml.safe_load(f)

    return Config.model_validate(data)
