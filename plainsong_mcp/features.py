"""Sixteen numbers per bar — re-exported from the compiler.

This was 300 lines duplicated byte-for-byte with `plainsong/features.py`, which
is exactly the failure "one of everything" exists to prevent: two copies of one
analysis, free to drift, with nothing in either repository able to notice when
they did.

Nothing about it was ever protocol-shaped. It reads an arrangement and describes
each bar — density, register, tessitura, the proportion of onsets on the beat —
which is a fact about music rather than about MCP, so it belongs beside
`notation/` and `perform/` in the compiler. It moved there, and `plainsong`
1.1.0 is the first release that publishes it.

This module remains as a re-export rather than being deleted, because
`plainsong_mcp.features` is imported by `tools.py`, by `selfcheck.py` and by the
test suite: a name that already works should keep working. The code now exists
once, which was the point.
"""

from __future__ import annotations

from plainsong.features import (
    BASS_CEILING,
    BEAT,
    FEATURE_NAMES,
    REFERENCES,
    BarFeatures,
    bar_count,
    bar_length,
    extract,
    format_table,
    summarise,
)

__all__ = [
    "BASS_CEILING",
    "BEAT",
    "FEATURE_NAMES",
    "REFERENCES",
    "BarFeatures",
    "bar_count",
    "bar_length",
    "extract",
    "format_table",
    "summarise",
]
