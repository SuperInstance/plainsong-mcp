#!/usr/bin/env python3
"""Offline dry-run: simulate the full 10-stitch loop without touching the live
ensemble session — same eye logic, same grower logic, analysis via MCP on
inline content. Used to calibrate the grower's vocabulary cells. The live run
then exercises the real seam (session writes, separate processes, logs)."""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feats, grower
import statistics as st

HDR = ("**TRACK: probe**\n[MetaData]\nkey: C | tempo: 100 | swing: 0% | "
       "subdivision: 8th\ntime: 4/4\n\n")

canon = {}
for p in sorted(glob.glob(os.path.join(os.path.dirname(__file__), feats.CANON_DIR, "*.song"))):
    canon[os.path.basename(p)] = feats.analyze_mean({"path": os.path.abspath(p)})["mean"]
centroid = {f: st.mean(c[f] for c in canon.values()) for f in feats.FEATURES}
cstd = {f: max(st.pstdev([c[f] for c in canon.values()]), feats.STD_FLOOR) for f in feats.FEATURES}

def d6(m): return sum(((m[f]-centroid[f])/cstd[f])**2 for f in feats.FEATURES) ** 0.5
def biggest_gap(m): return max(feats.FEATURES, key=lambda f: abs(m[f]-centroid[f])/cstd[f])

levels = {"air": 0, "sync": 0, "voicing": 0, "spread": 0}
rows = []
for n in range(1, 11):
    if n > 1:
        point = biggest_gap(rows[-1][1])
        crit = {"point_feature": point}
        what = grower.hear(levels, crit)
    else:
        what = "seed"
    m = feats.analyze_mean({"content": HDR + grower.compose(levels)})["mean"]
    rows.append((levels.copy(), m, what))
    print(f"s{n:2d} {levels} {what:45s} d={d6(m):5.2f}  " +
          "  ".join(f"{f[:4]}={m[f]:.3f}({abs(m[f]-centroid[f])/cstd[f]:4.2f}s)"
                    for f in feats.FEATURES))

print("\nper-feature distance-to-centroid sequences:")
mono = 0
for f in feats.FEATURES:
    seq = [abs(r[1][f]-centroid[f])/cstd[f] for r in rows]
    rises = [i for i in range(1, 10) if seq[i]-seq[i-1] > 0.02]
    big = [i for i in rises if seq[i]-seq[i-1] > 0.25*seq[0]]
    mono += (seq[-1] < seq[0] and len(rises) <= 1 and not big)
    viol = rises
    print(f"  {f:18s} " + " ".join(f"{x:5.2f}" for x in seq) + f"  violations@{viol}")
print("monotone:", mono, "/6 | curve:", [round(d6(r[1]), 2) for r in rows])
