"""
Variable definitions and translation.

This module translates user-friendly variable names (e.g. "2t", "tp")
into the corresponding variable names stored in the DestinE Climate DT
Zarr datasets.

The translation layer isolates the rest of the downloader from changes
in dataset variable naming.
"""

from __future__ import annotations

from collections.abc import Iterable

#
# Surface variables
#
# Keys are accepted aliases.
# Values are the variable names stored in the Zarr dataset.
#

SURFACE_VARIABLES: dict[str, str] = {

    #
    # Temperature
    #

    "2t": "t2m",
    "t2m": "t2m",
    "temperature": "t2m",

    #
    # Wind
    #

    "10u": "u10",
    "u10": "u10",

    "10v": "v10",
    "v10": "v10",

    #
    # Precipitation
    #

    "tp": "avg_tprate",
    "precipitation": "avg_tprate",

    #
    # Surface solar radiation
    #

    "ssr": "avg_sdswrf",
    "surface_solar_radiation": "avg_sdswrf",

}

#
# Pressure-level variables
#
# These are not used in v0.2.0 yet, but defining them now means
# v0.3 can add pressure-level downloads with minimal changes.
#

PRESSURE_VARIABLES: dict[str, str] = {

    "t": "t",
    "temperature": "t",

    "r": "r",
    "relative_humidity": "r",

}


#
# Reverse lookup for logging and output names.
#

CANONICAL_TO_SHORT: dict[str, str] = {

    "t2m": "2t",
    "u10": "10u",
    "v10": "10v",
    "avg_tprate": "tp",
    "avg_sdswrf": "ssr",

    "t": "t",
    "r": "r",

}


def translate(
    requested: Iterable[str],
    mapping: dict[str, str],
) -> list[str]:
    """
    Translate user-requested variable names into dataset variable names.

    Parameters
    ----------
    requested
        Variable names from the configuration.

    mapping
        Translation dictionary, typically SURFACE_VARIABLES or
        PRESSURE_VARIABLES.

    Returns
    -------
    list[str]
        Dataset variable names.

    Raises
    ------
    KeyError
        If an unknown variable is requested.
    """

    translated: list[str] = []

    for variable in requested:

        key = variable.lower()

        try:
            translated.append(mapping[key])

        except KeyError:

            valid = ", ".join(sorted(mapping))

            raise KeyError(
                f"Unknown variable '{variable}'. "
                f"Valid names are: {valid}"
            ) from None

    #
    # Remove duplicates while preserving order.
    #

    return list(dict.fromkeys(translated))


def short_name(variable: str) -> str:
    """
    Convert a dataset variable name back to a familiar short name.

    Examples
    --------
    >>> short_name("t2m")
    '2t'

    >>> short_name("avg_tprate")
    'tp'
    """

    return CANONICAL_TO_SHORT.get(variable, variable)

def test_translate():
    assert translate(["2t"], SURFACE_VARIABLES) == ["t2m"]

def test_duplicate():
    assert translate(["2t", "t2m"], SURFACE_VARIABLES) == ["t2m"]

def test_short_name():
    assert short_name("avg_tprate") == "tp"

__all__ = [
    "SURFACE_VARIABLES",
    "PRESSURE_VARIABLES",
    "translate",
    "short_name",
]
