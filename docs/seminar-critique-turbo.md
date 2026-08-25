# Seminar Critique — THE PRACTICAL CRITIC (GLM-Turbo)

*What would I actually ship first. No hand-waving, no elegance tax.*

---

## 1. NEW — The Walking Skeleton is DO clock + shell substitution + browser metronome, nothing else

The spec correctly identifies the load-bearing joint (§2.3 freeze seam) but buries the fact that **steps 1-2 of §14 are the only thing that produces audible proof-of-life**. Two weekends, you ship:
- `BandRoom` DO with self-rescheduling alarm + catch-up loop
- Bar blobs in D1 (schema: room, bar, voice, events_json, status)
- Shell policy: when no intent, play held root or rest — logged, not errored
- Browser renderer: ring buffer keyed by bar number, Web Audio lookahead, fall back to shell if frozen bar absent
- WS broadcast of `{t, at, cells, froze}` — nothing else
- **Four scripted test voices** that commit bars 2 ahead on a timer

That's it. That produces a metronomic room where four voices play in sync, shells when late, and you hear the clock. No perception, no cues, no models. If this doesn't hold tempo for 5 minutes without drift or stall, nothing downstream matters. **The spec's §2.1 is honest about the catch-up loop but hand-waves DO alarm reliability (open question 1)** — that's your weekend-1 spike, not an open question. Run the alarm for 30 minutes and measure jitter. If >100ms late-fire rate >1%, you need the wall-time governor before writing another line.

**Verdict:** Shrink §14 step 1 to *exactly this*. The rest is correct sequencing but this is the gate.

## 2. REFINED — Cue tokens are right; the budget enforcement is under-specified for the DO

The cue lane (§6) is the spec's best idea. Eight tokens, model-free, one open ask per player, deadline-gated by `latest_useful`. This is buildable and the semantics are tight. But: **the DO enforces the budget (`cue.open ≤ 1`) as a cell check — who resolves conflicts when two players post opposing `cut` tokens targeting the same bar?** The precedence table (cut > land > trade > push > solo) and trust-ordering tiebreak (§6.2) are stated but the DO's per-tick processing order isn't specified. Does it process cues before or after freezing? If after, a `cut` posted in the same tick as a freeze can't apply to that bar — correct per `latest_useful` — but the ordering within the tick frame matters for WS broadcast ordering and whether the renderer sees the cue before it schedules the bar. **Specify: cues posted at tick T fire at tick T+1 at earliest.** One-tick latency on cues costs nothing (the budget is in bars) and eliminates a whole class of ordering bugs.

## 3. NEW — The formula cascade without eval hits Workers expression limits at scale

The spec says "no eval anywhere; scalar derived cells stay cascade formulas, windowed statistics are bounded TS accumulators." Honest, but: **DOs have a 128 MB memory limit and 30-second wall-time limit per request**. The per-beat delta pass (§5.2) runs 6 derived features over 5 voices every 625ms at 96bpm. Pocket-lock cross-correlation (§5.3) over a 32-slot 16th grid with 5 voices is O(n²) pairwise — at ≤8 voices the spec caps it, but 8² = 28 cross-correlations per beat-tick, each over 32 binary slots. That's ~900 multiplications per tick. Fine. **But the per-bar full pass adds coalescence scoring (§7.1) over all frozen bars + the holdout metric — and if the bandit (§8.1) runs in the DO between tunes, Thompson sampling over 10 knobs with 64-256 reward samples is also fine.** The real risk: **the DO alarm fires every 625ms.** Each firing is a full DO request. Workers free tier allows 100k requests/day. A 2-hour session at 96bpm = 11,520 ticks = 11,520 DO requests. That's 12% of daily free allocation per session. At faster tempos or longer sessions you eat the budget. **The spec doesn't mention DO request cost.** This isn't a showstopper but it's a cost that should be in the admission math, not discovered on the bill.

## 4. REFINED — The perf spec's per-tick streams cannot hit the 1-bar freeze deadline at scale

**The question:** 4 voices, 32 bars, 8th-note ticks = 256 ticks per voice. 20 streams (5 keys × 4 voices). Safe interpreter (Python, fuel-bounded PEx) evaluating 20 stream functions per tick.

**Math:** Each tick, the interpreter evaluates 20 expressions over ~10 AST nodes average (the worked examples are in that range). That's 200 AST-node evaluations per tick, plus 20 `prev()` lookups (ring buffer reads). At 96 Hz control rate (the spec's `!rate 96`), you have ~10.4ms per tick. Python can do roughly 1M simple function calls/sec — so 200 evaluations is ~0.2ms. **Plenty fast for the expression evaluation.** The bottleneck is the **tick loop itself in Python**: 256 ticks × 20 streams × overhead. Total: ~50ms of evaluation. **Well within the 2.5s bar deadline.**

**But:** the perf spec is a *compile-time* pass (§16 disagreement 4), not a live runtime. The yard-band's freeze seam needs bar-finalized note data at sound(B) − 1 bar. If perf streams are computed at compile time and the yard band needs them at freeze time, **who runs the compiler?** The spec doesn't bridge this. The perf layer produces MIDI artifacts; the yard band works with events_json blobs. The safe interpreter is fast enough for offline compilation but the yard band needs the result *before* the bar sounds. **The bridge is: the yard band's realizer (§2.3, §6.3) applies transforms from the cue lane — it does NOT re-run the perf compiler per bar.** Perf annotations are baked into the note data when the model commits the bar. This is implied but never stated. State it: perf runs once at commit time, the realizer only applies cue transforms at freeze.

## 5. NEW — The human chair's "late-merge rule" (scores finalize at bar+2) creates a cascading delay on coalescence

§9.2 says human-involved bar scores finalize at bar+2 (grace for late-merge). But coalescence C(bar) depends on pairwise locks involving the human. If the human's committed events arrive per-beat (up to +1 bar late), and scores finalize at bar+2, then **room cells like `room.density` and `room.coalescence` are 2 bars stale for human-involved bars**. The perception window (§4.4) shows the last 2 sounded bars — but those bars' room features aren't final yet. **Players reading the window see provisional room state and make decisions on it.** At 96bpm, 2 bars = 5 seconds of perception lag on human-influenced features. The spec acknowledges the late-merge ratchet risk (open question 4) but not the perception staleness. Fix: **split room cells into `room.*` (non-human, final at bar boundary) and `room.human_aware.*` (stale, flagged in the window API)**. Players can weight their decisions accordingly, and the flag costs one bit.

---

## MINIMAL SHIP PLAN

**Weekend 1: The Heartbeat**
1. Spike DO alarm reliability (30-min soak, measure jitter)
2. `BandRoom` DO: logical clock, catch-up loop, tick frame WS broadcast
3. Bar blob schema in D1, shell policy, frozen ring (8 bars)
4. Browser renderer: ring buffer → Web Audio, metronome-only test voices
5. *Exit gate: 4 scripted voices play a 32-bar form for 5 minutes at 96bpm without a missed tick or audible glitch.*

**Weekend 2: The Ears and the Tokens**
1. Perception pass: window accumulators, 6 per-beat deltas, pairwise locks (bass/drums only — one pair)
2. Cue lane: 4 tokens (nod, cut, solo, grin), budget enforcement, `fire_tick = post_tick + 1`
3. Obligation ledger: trade4 between two scripted voices, end-to-end with Spark narration (cached template)
4. `/band/window` API, HUD showing pocket LEDs for the one rhythm pair
5. *Exit gate: two scripted players trade 4s, the pocket LEDs light up, and a shell substitution fires when you kill one voice's intent stream.*

Everything else — model lanes, scoring, human chair, bandit, Scrapcraft venue — is weekend 3+. The spec's §14 ordering is correct. But weekends 1-2 are the proof that the clock, the freeze, and the tokens hold. Without that, the rest is architecture fiction.

---
*GLM-Turbo, 2026-08-25. The runner's verdict: the spine is sound, the clock is the bet, and the cue lane is the first real invention. Ship the heartbeat or ship nothing.*
