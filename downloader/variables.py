"""
Variable aliases.

Allows the configuration to use familiar ECMWF short names.
"""

VARIABLE_ALIASES = {
    "2t": "t2m",
    "10u": "u10",
    "10v": "v10",
    "tp": "avg_tprate",
    "ssr": "avg_snswrf",
}


def translate(names):
    """
    Translate ECMWF-style names to Climate DT names.
    """

    return [
        VARIABLE_ALIASES.get(name, name)
        for name in names
    ]
