#!/usr/bin/env python3
"""THE GROWER — room 1. A separate process with its own notes and state.

Deliberately naive seed: the conservatory body — plain quarter-note root-
position block chords, one chord per bar, no rests, flat dynamics. Each stitch
it hears the eye's ONE point (feature language only — it has never seen the
canon) and answers by deepening ONE layer of its small, cumulative move
vocabulary. In-context iteration, not learning; the point is the loop.

Layers are FRACTIONAL: a move is first tried on a few bars, then spreads.
That is how a real player tries on a new habit — and it keeps each stitch's
step small enough to be steered by one point of critique.

  air     0-4  breathing: quarter grid -> half+quarters -> sparse -> thinner
  sync    0-2  off-beat lean + single-note anticipation of the next change
  voicing 0-4  quartal voicings, adopted bar by bar (1/4, 1/2, 3/4, all)
  spread  0-2  hands apart: bass pedal + octave lift, adopted bar by bar

Run as:  grower.py <stitch_dir> <rooms_dir> <stitch_no>
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feats

PROG = [("C", "maj7"), ("A", "m7"), ("D", "m7"), ("G", "dom7"),
        ("C", "maj7"), ("F", "maj7"), ("D", "m7"), ("G", "dom7"),
        ("E", "m7"), ("A", "dom7"), ("D", "m7"), ("G", "dom7"),
        ("C", "maj7"), ("F", "maj7"), ("G", "dom7"), ("C", "maj7")]
ROOT = {"C": 48, "D": 50, "E": 52, "F": 53, "G": 43, "A": 45}

CLOSE = {"maj7": (0, 4, 7, 11), "m7": (0, 3, 7, 10), "dom7": (0, 4, 7, 10)}
QUART = {"maj7": (4, 9, 14, 19), "m7": (7, 12, 17, 22), "dom7": (2, 6, 10, 15)}

# air rung -> (slots on deep bars, deep-bar fraction, thin the stack)
# thinning drops the FIFTH (keeps root-3rd-7th: the color survives)
AIR = {0: ([0, 2, 4, 6], 0.0, False),
       1: ([0, 4, 6],    1.0, False),
       2: ([0, 6],       0.5, False),
       3: ([0, 6],       1.0, False)}
SYNC_CELL = [1, 6]           # off-beat lean; sync rung -> fraction of bars
MOVE_MAP = {
 "note_density":      ("air", ["sync", "voicing"]),
 "rest_ratio":        ("air", ["sync", "voicing"]),
 "syncopation":       ("sync", ["air", "voicing"]),
 "harmonic_tension":  ("voicing", ["spread", "sync"]),
 "register_spread":   ("spread", ["voicing", "air"]),
 "interval_size":     ("spread", ["voicing", "air"]),
}
CAPS = {"air": 3, "sync": 2, "voicing": 4, "spread": 2}

NAMES = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
def name(m):
    if m < 33: m += 12
    return f"{NAMES[m % 12]}{m // 12 - 1}"

def notes_for(root_pc, quality, quartal, thin=False):
    iv = list(QUART[quality] if quartal else CLOSE[quality])
    ns = [ROOT[root_pc] + i for i in iv]
    while max(ns) > 84:
        ns = [n - 12 for n in ns]
    return sorted(ns)

def spread_notes(ns, lifted):
    if not lifted:
        return ns
    out = [ns[0] - 12] + [n + 12 for n in ns[1:]]
    while max(out) > 88:
        out = [n - 12 if n == max(out) else n for n in out]
    return sorted(out)

def in_set(i, level, cap, phase):
    """even bar-membership: fraction level/cap of bars, rotated by phase."""
    if level <= 0:
        return False
    frac = level / cap
    return ((i * 7 + phase * 3) % 16) / 16 < frac

def bar_tokens(bar_idx, levels):
    root_pc, quality = PROG[bar_idx]
    nxt_root, nxt_q = PROG[(bar_idx + 1) % 16]
    sync_bar = in_set(bar_idx, levels["sync"], 2, phase=1)
    slots, deep_frac, thin = AIR[levels["air"]]
    deep_bar = ((bar_idx * 7) % 16) / 16 < deep_frac
    trailing = levels["air"] >= 1
    quartal = in_set(bar_idx, levels["voicing"], 4, phase=0)
    lifted = in_set(bar_idx, levels["spread"], 2, phase=2)

    ns = spread_notes(notes_for(root_pc, quality, quartal, thin), lifted)
    if sync_bar:
        slots = SYNC_CELL
        thin = False
    anti = None
    if sync_bar and 7 not in slots:
        nxt = sorted(notes_for(nxt_root, nxt_q, quartal=False, thin=True))
        anti = nxt[-1]  # single-note anticipation of the next change
    last = max(slots)
    toks = []
    for s in range(8):
        if s in slots:
            toks.append("-".join(name(n) for n in ns))
        elif anti is not None and s == 7:
            toks.append(name(anti))
        elif trailing and s > last:
            toks.append("(rest)")
        else:
            toks.append(".")
    return " ".join(toks)

def compose(levels):
    rows = [f"@piano | {bar_tokens(i, levels)} | vel: 70" for i in range(16)]
    return "[A]\n" + "\n".join(rows[:8]) + "\n[B]\n" + "\n".join(rows[8:])

def hear(levels, crit):
    feat = crit["point_feature"]
    layer, fallbacks = MOVE_MAP[feat]
    if levels[layer] >= CAPS[layer]:
        for fb in fallbacks:
            if levels[fb] < CAPS[fb]:
                layer = fb
                break
        else:
            return f"all layers deep (heard {feat}); consolidation stitch, no change"
    levels[layer] = min(levels[layer] + 1, CAPS[layer])
    return f"deepened '{layer}' to {levels[layer]}/{CAPS[layer]} (heard: {feat})"

def main():
    stitch_dir, rooms_dir, stitch_no = sys.argv[1], sys.argv[2], int(sys.argv[3])
    state_path = os.path.join(rooms_dir, "room-grower", "grower-state.json")
    levels = {"air": 0, "sync": 0, "voicing": 0, "spread": 0}
    if os.path.exists(state_path):
        levels = json.load(open(state_path))["levels"]

    heard, applied = "seed: no critique yet — play the conservatory body", "seed (all layers 0)"
    if stitch_no > 1:
        crit = json.load(open(os.path.join(stitch_dir, "critique.json")))
        heard = crit["text"]
        applied = hear(levels, crit)

    content = compose(levels)
    feats.call("ensemble_join", {"session": feats.SESSION, "voice": "@piano", "agent": "grower"})
    read = json.loads(feats.call_text("ensemble_read", {"session": feats.SESSION, "voice": "@piano", "agent": "grower"}))
    w = feats.call_text("ensemble_write_part", {
        "session": feats.SESSION, "voice": "@piano", "agent": "grower",
        "base_version": read["you"]["base_version"], "content": content,
        "summary": f"stitch {stitch_no}: {applied}"})

    json.dump({"levels": levels, "stitch": stitch_no}, open(state_path, "w"))
    with open(os.path.join(rooms_dir, "room-grower", "notes.md"), "a") as fh:
        fh.write(f"- stitch {stitch_no}: HEARD «{heard[:150]}» -> {applied}; "
                 f"write: {w.strip()[:50]}\n")

if __name__ == "__main__":
    main()
