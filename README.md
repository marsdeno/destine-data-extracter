# DestinE Climate DT Downloader

A lightweight Python tool for extracting regional subsets from the
Destination Earth (DestinE) Climate Digital Twin (Climate DT) datasets
hosted on the Earth Data Hub.

The downloader accesses remote Zarr datasets directly using xarray,
downloads only the requested variables, years and spatial region, and
writes annual NetCDF files.

---

## Philosophy

The downloader performs one extraction task at a time:

    one variable
    ×
    one calendar year
    ×
    one geographical region

This keeps memory usage low, makes interrupted runs easy to resume,
and provides a natural unit for future parallel execution.

## Features

- Authentication using `.netrc`
- Direct access to remote Zarr datasets
- Regional subsetting
- Annual NetCDF output
- Automatic variable name translation
- Resumable downloads
- Automatic retries for transient network failures
- Compressed NetCDF output

---

## Current status

Version: **0.2**

Implemented:

- Surface dataset
- Annual extraction
- Variable aliases
- Retry logic
- Safe NetCDF writing

Planned:

- Pressure-level dataset
- Command-line interface
- Parallel downloads

---

## Installation

Create a virtual environment.

Install the required packages.

```bash
pip install \
    xarray \
    dask \
    zarr \
    aiohttp \
    fsspec \
    netCDF4 \
    pyyaml \
    pydantic
```

---

## Authentication

Create a `.netrc` file in your home directory.

Example:

```text
machine api.earthdatahub.destine.eu
login apikey
password YOUR_API_KEY
```

Permissions should be

```bash
chmod 600 ~/.netrc
```

---

## Configuration

Example:

```yaml
datasets:

  surface:
    url: https://...

  pressure:
    url: https://...

bbox:

  west: -5
  east: 9
  south: 41
  north: 51

years:

  start: 2035
  end: 2035

surface:

  - 2t
  - 10u
  - 10v
  - tp
  - ssr

pressure: []

pressure_levels: []

output: output

download:

  retries: 3
  retry_delay: 10
```

---

## Variable aliases

The Climate DT uses slightly different variable names from standard
ECMWF products.

| Requested | Climate DT |
|-----------|------------|
| 2t | t2m |
| 10u | u10 |
| 10v | v10 |
| tp | avg_tprate |
| ssr | avg_snswrf |

Note that `avg_tprate` is a mean precipitation rate rather than an
accumulated precipitation field.

---

## Running

```bash
python download.py
```

---

## Output

Files are organised by dataset, variable and year.

```
output/

    surface/

        t2m/
            2035.nc

        u10/
            2035.nc

        avg_tprate/
            2035.nc
```

Each file contains

- one variable
- one calendar year
- one spatial region

---

## Project structure

```
download.py

config.yaml

downloader/

    config.py
    dataset.py
    retry.py
    subset.py
    tasks.py
    variables.py
    writer.py
```

---

## Design principles

The downloader is designed around a small unit of work:

> one variable × one year

This allows

- easy restart
- automatic resume
- future parallel execution
- minimal loss after network failures

---

## Known limitations

- Pressure-level extraction is not yet implemented.
- Retry logic currently applies only during NetCDF writing.
- The downloader assumes the requested variables exist in the selected dataset.

---

## Licence

TBD
