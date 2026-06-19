from pathlib import Path

from dask.diagnostics import ProgressBar


def write_netcdf(
    ds,
    filename,
):

    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)

    encoding = {

        variable: {

            "zlib": True,

            "complevel": 4,

        }

        for variable in ds.data_vars

    }

    with ProgressBar():

        ds.to_netcdf(
            filename,
            encoding=encoding,
        )
