#!/usr/bin/env python3
"""Seamstress gate-1 harness — ONE HOOP, ONE SEAM, TEN STITCHES.

Two rooms are two plain processes with separate working notes (rooms/room-*).
The seam is the filesystem + MCP: the grower writes notation into the ensemble
session; the harness materialises the take + perception; the blind eye reads
ONLY notation+features and speaks one point. Growth question: does the loop
move the take toward the canon centroid, measurably, stitch over stitch?

Run from the repo root:  python3 stitch/harness.py
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feats

REPO = "/home/eileen/projects/plainsong-mcp"
STITCH = os.path.join(REPO, "stitch")
RUNS = os.path.join(STITCH, "runs")
ROOMS = os.path.join(STITCH, "rooms")
LOG = os.path.join(STITCH, "stitch-log.jsonl")

def open_hoop():
    r = feats.call("ensemble_open", {
        "session": feats.SESSION, "title": "Seamstress Gate 1 — one hoop",
        "key": "C", "tempo": 100, "meter": "4/4", "subdivision": "8th",
        "sections": [{"name": "A", "description": "First half - 8 bars", "bars": 8},
                     {"name": "B", "description": "Second half - 8 bars", "bars": 8}],
        "voices": ["@piano"]})
    return r["content"][0]["text"]

def stitch_dir(n):
    d = os.path.join(RUNS, f"stitch-{n:02d}")
    os.makedirs(d, exist_ok=True)
    return d

def one_stitch(n, prev_vec):
    d = stitch_dir(n)
    if n > 1:  # hand the previous critique across the seam to the grower
        import shutil
        shutil.copy(os.path.join(RUNS, f"stitch-{n-1:02d}", "critique.json"),
                    os.path.join(d, "critique.json"))
    # ROOM 1: the grower (subprocess; own notes, own MCP connection)
    out = subprocess.run([sys.executable, os.path.join(STITCH, "grower.py"), d, ROOMS, str(n)],
                         capture_output=True, text=True, cwd=REPO)
    if out.returncode:
        raise RuntimeError(f"grower failed @ {n}: {out.stderr[-800:]}")

    # materialise the take from the session (notation handoff to the eye)
    read = json.loads(feats.call_text("ensemble_read", {"session": feats.SESSION}))
    part = open(os.path.join(read["directory"], "parts", "piano.song")).read()
    take = ("**TRACK: seamstress-gate1 take**\n[MetaData]\n"
            "key: C | tempo: 100 | swing: 0% | subdivision: 8th\ntime: 4/4\n\n"
            "[A] (8 bars)\n" + "\n".join(part.splitlines()[1:9]) +
            "\n[B] (8 bars)\n" + "\n".join(part.splitlines()[10:]))
    take_path = os.path.join(d, "take.song")
    open(take_path, "w").write(take)

    mean = feats.analyze_mean({"path": take_path})["mean"]
    json.dump({"mean": mean}, open(os.path.join(d, "take-features.json"), "w"))

    # ROOM 2: the eye (subprocess; sees ONLY take.song + take-features.json)
    out = subprocess.run([sys.executable, os.path.join(STITCH, "eye.py"), d, ROOMS],
                         capture_output=True, text=True, cwd=REPO)
    if out.returncode:
        raise RuntimeError(f"eye failed @ {n}: {out.stderr[-800:]}")
    crit = json.load(open(os.path.join(d, "critique.json")))

    v = feats.vec6(mean)
    if prev_vec:
        moved = [f"{feats.FEATURES[i]}: {prev_vec[i]:+.3f} -> {v[i]:+.3f}"
                 for i in sorted(range(6), key=lambda i: -abs(v[i] - prev_vec[i]))[:3]]
    else:
        moved = ["seed (no previous)"]
    digest = " | ".join(part.splitlines()[1].split("|")[1:3]).strip()[:70]

    return {"stitch": n, "notation_digest": digest,
            "feature_vector_summary": dict(zip(feats.FEATURES, v)),
            "critique": crit["text"], "features_moved": moved,
            "centroid_distance": crit["centroid_distance"]}, v

def measure(rows):
    import statistics as st
    canon = {}
    import glob
    for p in sorted(glob.glob(os.path.join(STITCH, feats.CANON_DIR, "*.song"))):
        canon[os.path.basename(p)] = feats.analyze_mean({"path": os.path.abspath(p)})["mean"]
    centroid = {f: st.mean(c[f] for c in canon.values()) for f in feats.FEATURES}
    std = {f: max(st.pstdev([c[f] for c in canon.values()]), feats.STD_FLOOR)
           for f in feats.FEATURES}
    curve = [row["centroid_distance"] for row in rows]
    per_feat = {}
    for f in feats.FEATURES:
        seq = [abs(row["feature_vector_summary"][f] - centroid[f]) / std[f] for row in rows]
        rises = [i for i in range(1, len(seq)) if seq[i] - seq[i - 1] > 0.02]
        big = [i for i in rises if seq[i] - seq[i - 1] > 0.25 * seq[0]]
        ok = seq[-1] < seq[0] and len(rises) <= 1 and not big
        per_feat[f] = {"seq": [round(x, 3) for x in seq], "rises": rises,
                       "start": round(seq[0], 3), "end": round(seq[-1], 3),
                       "monotone": ok}
    monotone = sum(1 for f in per_feat.values() if f["monotone"])
    verdict = "GATE-PASS" if (monotone >= 4 and curve[-1] < curve[0]) else "GATE-FAIL"
    return {"centroid": {f: round(centroid[f], 3) for f in feats.FEATURES},
            "curve": curve, "per_feature": per_feat,
            "monotone_features": monotone, "verdict": verdict}

def main():
    os.makedirs(RUNS, exist_ok=True)
    open(LOG, "w").close()
    print("hoop:", open_hoop()[:120].replace("\n", " "))
    rows, prev = [], None
    for n in range(1, 11):
        row, prev = one_stitch(n, prev)
        rows.append(row)
        with open(LOG, "a") as fh:
            fh.write(json.dumps(row) + "\n")
        print(f"stitch {n:2d}  d={row['centroid_distance']:6.3f}  "
              f"{row['critique'][:90]}")
    m = measure(rows)
    json.dump(m, open(os.path.join(STITCH, "measurement.json"), "w"), indent=1)
    print("\ncurve:", m["curve"])
    print("per-feature rises:", {f: v["rises"] for f, v in m["per_feature"].items()})
    print("monotone:", m["monotone_features"], "/6 ->", m["verdict"])

    r = feats.call_text("ensemble_render", {"session": feats.SESSION, "audio": True})
    print("render:", r.strip()[:200])
    read = json.loads(feats.call_text("ensemble_read", {"session": feats.SESSION}))
    src = os.path.join(read["directory"], "score.song")
    open(os.path.join(STITCH, "final-take.song"), "w").write(open(src).read())

if __name__ == "__main__":
    main()
