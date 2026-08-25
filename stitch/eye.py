#!/usr/bin/env python3
"""THE EYE — room 2 (blind critic). A separate process with its own notes.

BLIND BY CONSTRUCTION: receives ONLY  <stitch_dir>/take.song  and
<stitch_dir>/take-features.json  (notation + perception). It never sees the
grower's reasoning, the grower's notes, prior critiques, or the stitch number.
It owns the canon, judges "would this fit?", and speaks ONE directional point
in feature language — citing the nearest canon neighbor by feature distance.

Run as:  eye.py <stitch_dir> <rooms_dir>
Writes:  <stitch_dir>/critique.json, appends <rooms_dir>/room-eye/notes.md
"""
import json, os, sys, glob, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feats

FIT_VERDICTS = [(1.5, "no"), (0.8, "not-yet"), (0.45, "getting-close"), (0.0, "close")]

POINT = {
 "note_density":   ("above", "too much ink — every slot speaks; let bars breathe with fewer attacks"),
 "syncopation":    ("below", "attacks all land square on the grid; let changes arrive off the beat"),
 "register_spread":("below", "everything lives in one narrow band; the hands sit too close together"),
 "rest_ratio":     ("below", "no silence anywhere; leave air inside and between phrases"),
 "harmonic_tension":("below","the harmony sits plain; colour tones and gentle dissonance are missing"),
 "interval_size":  ("below", "voicings cluster in close position; open the intervals between hands"),
}

def canon_vectors():
    vecs = {}
    for path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), feats.CANON_DIR, "*.song"))):
        d = feats.analyze_mean({"path": os.path.abspath(path)})
        name = os.path.basename(path).replace(".song", "")
        vecs[name] = d["mean"]
    return vecs

def main():
    stitch_dir, rooms_dir = sys.argv[1], sys.argv[2]
    take = json.load(open(os.path.join(stitch_dir, "take-features.json")))["mean"]

    canon = canon_vectors()
    centroid = {f: st.mean(c[f] for c in canon.values()) for f in feats.FEATURES}
    canon_std = {f: max(st.pstdev([c[f] for c in canon.values()]), feats.STD_FLOOR)
                 for f in feats.FEATURES}

    def d6(m):
        return sum(((m[f] - centroid[f]) / canon_std[f]) ** 2 for f in feats.FEATURES) ** 0.5

    # nearest canon neighbor by feature distance over the 6 tracked features
    nearest = min(canon, key=lambda n: d6(canon[n]))
    d_near = d6(canon[nearest])

    # ONE directional point: the largest normalized gap
    gaps = {f: abs(take[f] - centroid[f]) / canon_std[f] for f in feats.FEATURES}
    point_feat = max(gaps, key=gaps.get)
    side, phrase = POINT[point_feat]
    lo = min(c[point_feat] for c in canon.values())
    hi = max(c[point_feat] for c in canon.values())

    d_total = d6(take)
    fit = next(v for t, v in FIT_VERDICTS if d_total > t)

    critique = {
        "fit": fit,
        "nearest": nearest,
        "nearest_distance": round(d_near, 3),
        "point_feature": point_feat,
        "take_value": round(take[point_feat], 3),
        "canon_range": [round(lo, 3), round(hi, 3)],
        "centroid_distance": round(d_total, 3),
        "text": (f"FIT: {fit}. Nearest canon neighbor: {nearest} "
                 f"(d={d_near:.2f}). ONE POINT — {point_feat.replace('_',' ')} "
                 f"sits at {take[point_feat]:.3f}, {side} the canon neighborhood "
                 f"({lo:.3f}–{hi:.3f}): {phrase}."),
    }
    with open(os.path.join(stitch_dir, "critique.json"), "w") as fh:
        json.dump(critique, fh, indent=1)

    notes = os.path.join(rooms_dir, "room-eye", "notes.md")
    with open(notes, "a") as fh:
        fh.write(f"- judged a take: fit={fit}, d={d_total:.2f}, nearest={nearest} "
                 f"({d_near:.2f}); point -> {point_feat} "
                 f"(take {take[point_feat]:.3f} vs canon {lo:.3f}-{hi:.3f})\n")

if __name__ == "__main__":
    main()
