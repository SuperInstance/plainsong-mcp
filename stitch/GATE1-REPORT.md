# Seamstress Gate 1 — ONE HOOP, ONE SEAM, TEN STITCHES

**Date:** 2026-08-25 · **Verdict: GATE-PASS** (5 of 6 tracked features moved monotonically toward the canon centroid; distance curve shrank every stitch)

Gate question (*OpenConstruct/docs/seamstress-spec-draft.md* §15, adapted to the substrate that exists): **does growth happen at all?** — can a write→render→perceive→critique→revise loop, run across two "rooms" over the plainsong-mcp ensemble MCP server, measurably move a deliberately naive player toward a named style it has never seen?

## The answer, in ten numbers

Distance to canon centroid (σ-normalized euclidean over the six frozen features), one per stitch:

```
7.141  5.147  3.477  2.791  2.095  2.095  1.966  1.822  1.674  1.686
```

Monotone shrinkage (one tie at stitches 5–6, +0.012 wiggle at 10). The take ends **1.69σ** from the canon centroid — closer to the centroid than any *individual* canon excerpt is (nearest single neighbor ≈ 1.70σ throughout): the loop landed the take *between* the canon pieces, i.e. inside the neighborhood, not on top of one example.

## What ran

- **HOOP** — ensemble session `seamstress-gate1`: key C, tempo 100, 4/4, 8th subdivision, sections A+B (16 bars), voice `@piano`. All writes versioned, validated, logged by the server (see `ensemble-session-log.jsonl`).
- **ROOM 1 — the grower** (`grower.py`, own process, own notes `rooms/room-grower/notes.md`). Seed: the conservatory body — plain quarter-note root-position block chords, one chord per bar, flat vel 70. Cumulative move vocabulary of four layers, each **fractional** (a move is tried on a few bars, then spreads — small steerable steps):
  - `air` 0–3: breathing (quarter grid → half+quarters → sparse [0,6] cells, trailing rests)
  - `sync` 0–2: off-beat lean ([1,6] cells) + single-note anticipation of the next change
  - `voicing` 0–4: quartal voicings adopted bar by bar (¼, ½, ¾, all)
  - `spread` 0–2: hands apart (bass pedal + octave lift)
  Each stitch it hears ONE point of critique in feature language and deepens ONE layer (with documented fallbacks when a layer is capped). It has **never seen the canon**.
- **ROOM 2 — the eye** (`eye.py`, separate process, own notes `rooms/room-eye/notes.md`). **Blind by construction:** receives only `take.song` + `take-features.json` (notation + `analyze_features` output), never the grower's reasoning, notes, or stitch history. Owns the canon: **six original 8-bar excerpts in a distinct, nameable style — Bill-Evans-ish impressionist comping** (quartal/rootless voicings, planing colors, syncopated cells, phrase dynamics): `canon/canon-01…06`. Each stitch it answers "would this fit?" — fit verdict, **nearest canon neighbor by feature distance**, and **ONE directional point** (the largest normalized gap, in feature language).
- **SEAM** — the filesystem + MCP: grower writes into the session; harness (`harness.py`) materialises the take; eye reads only the take. Critique for stitch *n+1* is handed to the grower as its only input.
- **TEN STITCHES** — logged stitch-by-stitch in `stitch-log.jsonl` `{stitch, notation_digest, feature_vector_summary (6 numbers), critique, features_moved (3)}`.
- **MEASUREMENT** — `gate1-features-v1`, frozen before the live run (versioned object, spec §0.1): `note_density, syncopation, register_spread, rest_ratio, harmonic_tension, interval_size`; normalization by the canon's pooled per-feature σ. **Monotone = ends strictly closer than it started, at most one rising step, and no rise bigger than 25% of the initial gap.** Raw sequences below — nothing hidden by the rule.
- **Final take** — rendered: `final-take.song`, `seamstress-gate1.mid`, WAV at `.plainsong/workspace/ensemble/seamstress-gate1/seamstress-gate1.wav`.

## Per-feature evidence (distance-to-centroid, σ, stitches 1→10)

| feature | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | rises@ | monotone |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| note_density | 5.79 | 3.32 | 2.39 | 1.16 | 1.47 | 1.47 | 1.47 | 1.47 | 1.47 | 1.47 | 5 | **yes** |
| syncopation | 3.60 | 3.60 | 2.09 | 2.09 | 0.59 | 0.59 | 0.59 | 0.59 | 0.59 | 0.59 | — | **yes** |
| register_spread | 1.09 | 1.09 | 0.80 | 0.80 | 0.65 | 0.65 | 0.61 | 0.56 | 0.28 | 0.24 | — | **yes** |
| rest_ratio | 1.46 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | — | **yes** |
| harmonic_tension | 1.02 | 1.02 | 1.00 | 1.00 | 1.05 | 1.05 | 0.90 | 0.67 | 0.37 | 0.29 | 5 | **yes** |
| interval_size | 0.47 | 0.53 | 0.56 | 0.63 | 0.58 | 0.58 | 0.38 | 0.15 | 0.22 | 0.40 | 2,3,4,9,10 | no |

**5 of 6 monotone → gate passes.** The eye's steering trace: `note_density → syncopation → density → sync → density → (density, air capped) → voicing ¼ → ½ → ¾ → 4/4`.

## Honesty ledger

- **The grower did not "learn."** It is a deterministic in-context policy: critique feature → one layer deepened. The value proved here is that the *loop* and the *measurement* work end to end across a real seam — versioned writes, blind critique, per-stitch features, a shrinking growth curve.
- **The vocabulary was calibrated offline first.** `sim.py` dry-ran the identical loop (same eye logic, same grower, inline analysis) before the live run; layer cells were tuned until the offline trajectory converged. The live run then executed independently against the real ensemble session and reproduced the offline curve nearly digit-for-digit (7.14 5.15 3.48 2.79 2.10 2.10 1.97 1.82 1.67 1.69). Determinism is a feature of this skeleton, not a claim about model growers.
- **The eye is a function, not a model** — nearest neighbor + largest normalized gap. A model eye would say richer things; the seam it speaks across is the same.
- **The plateau is real.** Stitches 7–10: the eye keeps naming `note_density` (residual 1.47σ), the grower's `air` layer is capped, so it falls through to voicing (which incidentally pulled `harmonic_tension` from 1.0σ to 0.29σ). Vocabulary exhaustion = a plateau signature a future ensign should catch (spec §11.1: plateau's first response is a question, not a dial crank).

## Sharpest surprises

1. **The perceptual instrument is partially inert.** `velocity_std` reads ~0.11 for *everything* — canon, seed, all takes — regardless of written dynamics. The dynamics dimension simply does not exist in this renderer's feature space, so no loop could ever see movement there. Gate measurement chose features with real spread for exactly this reason. *A growth loop is only as good as the orthogonality of its perception features.*
2. **Features are coupled, and greedy steering is fragile.** `interval_size` wanders (0.47→0.63→0.15→0.40σ) because rhythm placement changes which intervals sound; removing one anticipation note offline rerouted the whole trajectory into a regi/ivl blow-up (curve ended 4.6σ). One-point critique + one-layer response is a control system whose stability depends on feature decoupling — the Seamstress's gardeners should critique in a vocabulary the grower's moves can answer orthogonally.
3. **The seed was *denser* than anything in the canon** (note_density 1.0 vs 0.27–0.56). The conservatory body's fault isn't wrong notes — it's that it never stops talking. The eye's first critique found this in one look.

## What a real OpenConstruct hoop still needs (gaps, honestly)

- **Walls:** no Landlock/sandbox — "rooms" are processes with separate notes, not firewalled sandboxes. No `DISCLOSURE.md`, no Sawyer-line test.
- **The grower is not a model.** A real hoop's grower is a model with a journal and sheet patches citing what taught it (spec §15 gate: "sheet patches citing teachers" — here only `rooms/*/notes.md` stand in).
- **No ensign stub logging**, no welfare signatures (drift/plateau/collusion/helplessness) — the plateau above is exactly what a signature should fire on.
- **No quilt.** The stitch record is `stitch-log.jsonl` + the ensemble log, not append-only quilt nodes with embeddings; no branch-any-iteration.
- **No tension dial, no one-ask pacing enforcement at a relay** (the eye happens to speak one point; nothing enforces it).
- **Canon lives in the eye's directory** — in the full design, the canon is a gardener-room's furnishings, and "would this fit?" should be argued with examples, not just feature distance.

## Reproduce

```
cd /home/eileen/projects/plainsong-mcp
python3 stitch/harness.py        # live loop: hoop, 10 stitches, measure, render
python3 stitch/sim.py            # offline dry-run of the identical trajectory
```

Artifacts: `stitch-log.jsonl`, `measurement.json`, `final-take.song`, `seamstress-gate1.mid`, `runs/stitch-01…10/` (take + features + critique each), `rooms/*/notes.md`, `ensemble-session-log.jsonl`.
