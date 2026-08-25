"""The perception instruments that keep a loop from steering blind.

The pulse-eye retrospective (tensor-midi, 2026-08-25) found the seam this
module exists to close. Every signal the eye needed -- the pocket lock that
was one bar of Groove among sixteen, the growth that was a monotone register
climb -- was already in the per-bar feature stream; the loop's *summaries*
(mode majority, channel count, the mean of each feature) averaged the signal
away. Two instruments fell into the same trap from opposite sides: one had a
channel that read zero in all twenty-nine states because its input lived
somewhere the notes never carried it, and another steered on two numbers that
moved together so tightly they were one dimension wearing two names. A
perceptual instrument has dead channels, and coupled ones, and you only find
either by running the loop -- so the loop gets instruments that look for
them.

Three tools live on top of this module:

* ``perception_trace`` -- the per-bar rows themselves, never a mean. The
  finding was not that the data was missing but that the summary path
  collapsed it; this is the path that does not.
* ``dimension_stats`` -- the compiler's generic annotation rows (``Breath:``,
  any name a composer can write), so an eye can see custom dimensions, not
  just velocity. Degrades with a readable error when the installed compiler
  does not publish them.
* ``perception_audit`` -- variance and correlation over the sixteen channels,
  and a verdict per channel: DEAD (no variance anywhere it can be measured),
  COUPLED (|r| > 0.9 with another channel -- one steering dimension, not
  two) or ALIVE. Orthogonality of steering channels is the difference
  between growing and stalling; this is the instrument that checks for it.

The statistics are deliberately plain -- variance, Pearson r, union-find over
coupled pairs -- because the point is not sophistication, it is that the
numbers a loop steers by are themselves measurements that can be wrong, and
the only defense is to measure the measurements.
"""

from __future__ import annotations

from typing import Any

from . import features as feat

ZERO_VARIANCE = 1e-9
"""Below this, a channel's variance counts as zero.

The features are rounded to two decimals, so a channel that varies at all
varies by at least 0.01 somewhere; anything smaller than this is arithmetic
dust, not signal.
"""

COUPLING = 0.9
"""|r| above which two channels are one steering dimension, not two."""


def channel_series(bars: list[Any]) -> dict[str, list[float]]:
    """Each feature's per-bar values, in :data:`~plainsong.features.FEATURE_NAMES` order."""
    return {
        name: [bar.values[name] for bar in bars]
        for name in feat.FEATURE_NAMES
        if bars and name in bars[0].values
    }


def variance(values: list[float]) -> float:
    """Population variance. Zero variance is the dead-channel signature."""
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / len(values)


def pearson(xs: list[float], ys: list[float]) -> float | None:
    """Correlation of two equal-length series, or None when it is undefined.

    Undefined means fewer than two points, or a series with no spread: the
    correlation of a dead channel with anything is not zero, it is *nothing*,
    and reporting a number there would be the summary path lying again.
    """
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    dx = [x - mx for x in xs]
    dy = [y - my for y in ys]
    denominator = (sum(d * d for d in dx) * sum(d * d for d in dy)) ** 0.5
    if denominator <= 0.0:
        return None
    return sum(a * b for a, b in zip(dx, dy, strict=True)) / denominator


def _groups(names: list[str], pairs: list[tuple[str, str]]) -> list[list[str]]:
    """Union-find over *names*: coupled channels share one steering dimension."""
    parent = {name: name for name in names}

    def find(name: str) -> str:
        while parent[name] != name:
            parent[name] = parent[parent[name]]
            name = parent[name]
        return name

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    clusters: dict[str, list[str]] = {}
    for name in names:
        clusters.setdefault(find(name), []).append(name)
    return [sorted(members) for _, members in sorted(clusters.items())]


def audit(views: dict[str, list[Any]]) -> dict[str, Any]:
    """Verdicts for the sixteen channels, over however the score can be heard.

    *views* maps a way of hearing the piece -- ``"(all)"`` for the whole
    texture, one entry per voice -- to its per-bar features. A channel is
    DEAD when it has no variance in *any* view: the whole texture may cancel
   two voices that each move, but a channel that never moves in any single
    voice never moves at all, and an ensemble loop steering on it is steering
    on a dial connected to nothing.

    Correlations are read from the whole-texture view, because that is what
    a bandleader steers. Two channels with |r| above :data:`COUPLING` are one
    steering dimension wearing two names; the audit groups them so the loop
    counts its real degrees of freedom, not its labels.
    """
    texture = views.get("(all)", [])
    series = channel_series(texture)
    per_voice = {name: channel_series(bars) for name, bars in views.items() if name != "(all)"}

    channels: dict[str, dict[str, Any]] = {}
    dead: list[str] = []
    for name in feat.FEATURE_NAMES:
        if name not in series:
            continue
        spread = variance(series[name])
        heard_anywhere = any(
            variance(view.get(name, [])) > ZERO_VARIANCE for view in per_voice.values()
        ) or spread > ZERO_VARIANCE
        entry: dict[str, Any] = {
            "variance": round(spread, 8),
            "std": round(spread**0.5, 6),
            "verdict": "ALIVE" if heard_anywhere else "DEAD",
        }
        if not heard_anywhere:
            dead.append(name)
        channels[name] = entry

    correlations: list[dict[str, Any]] = []
    coupled_pairs: list[tuple[str, str]] = []
    alive = [name for name in feat.FEATURE_NAMES if name in series and name not in dead]
    for i, a in enumerate(alive):
        for b in alive[i + 1 :]:
            r = pearson(series[a], series[b])
            if r is None:
                continue
            if abs(r) > COUPLING:
                coupled_pairs.append((a, b))
                correlations.append({"a": a, "b": b, "r": round(r, 3)})

    grouped = _groups(alive, coupled_pairs)
    coupled_names: set[str] = set()
    for members in grouped:
        if len(members) > 1:
            coupled_names.update(members)
            for name in members:
                channels[name]["verdict"] = "COUPLED"
                channels[name]["coupled_with"] = [m for m in members if m != name]

    independent = [members[0] for members in grouped if len(members) == 1]
    merged = [members for members in grouped if len(members) > 1]
    summary = (
        f"{len(series)} channels -> {len(independent) + len(merged)} steering dimensions "
        f"({len(dead)} dead, {len(coupled_names)} coupled into {len(merged)})"
    )
    return {
        "bars": len(texture),
        "views": sorted(views),
        "channels": channels,
        "correlations": correlations,
        "dead": dead,
        "coupled": merged,
        "independent": independent,
        "steering_dimensions": len(independent) + len(merged),
        "summary": summary,
    }
