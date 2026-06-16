import logging

from downloader.config import load_config
from downloader.dataset import ClimateDataset

logging.basicConfig(level=logging.INFO)

cfg = load_config("config.yaml")

surface = ClimateDataset(
    cfg.datasets.surface.url
)

ds = surface.open()

print(ds)

print("\nCoordinates")
print(ds.coords)

print("\nVariables")
print(list(ds.data_vars))
