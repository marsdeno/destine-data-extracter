from downloader.config import load_config

cfg = load_config("config.yaml")

print(cfg)

print(cfg.datasets.surface.url)
print(cfg.bbox)
