# Seminar Critique — GLM-5.2 as Outside Critic

*Cross-model architecture seminar, 2026-08-25. Adversarial review of three sibling
specs: plainsong perf-spec, ensemble-engine v0.1, yard-band v0.1. Protocol: max 5
points per spec, ranked, tagged NEW or REFINED, each directional. I earn my keep
by finding what review misses — so I went to the evidence files and the source
trees, not just the specs.*

**Evidence note:** `duke-lab/REPORT.md` does not exist. The duke-lab evidence is
`log.jsonl` + `manifest.json` + `score.song`: a **solo** session (one agent,
`band-glm`, @piano only, 16 bars / 116 notes, two writes, join→first-write
≈ 117 s, revision +147 s). That matters below — the only observed agent latencies
in the whole corpus are batch writes of 60–155 s, and nobody plays with anyone in
that session. the-tap-afterhours is the only multi-agent evidence, and its log
contradicts two claims the specs make about it (points E5, Y1).

---

## A. PLAINSONG PERF (`perf-spec-draft.md`)

### A1. [NEW — overengineering] Cut turing-completeness from v1. Recursion buys nothing the spec itself uses.
§7.2, §7.5, §18. Not one worked example (§11.1–11.7) uses recursion; every one is
closed-form synchronous dataflow (`sin`, `env`, `smoothstep`, `hash`). Yet
recursion drags in the entire fuel apparatus — fuel-error semantics, `fallback:`
emission rules, open question 8 ("should compile also fail?"), implementation
step 4 — a whole failure-mode axis servicing a capability with zero demonstrated
need. The honest sandbox story (§16.4) survives fine without it: purity +
determinism + bounded streams is already the guarantee that matters. **Fix:**
ship PEx first-order (a Lustre-class synchronous language, which is what §12
actually describes); add recursion only when a real perf file demands it, which
the category ledger will show. This deletes a failure mode, an open question,
and an implementation phase in one cut.

### A2. [NEW — seam] The engine's `intent_directive` has no consumer in this spec. The "contract" is a handshake with no hand.
Engine §0.3 and §3.1 define the seam as: cues emit intent directives
(`wants: {feature: velocity_mean, dir: down, window: 9-9}`, `keep_empty:
["9.2-9.4"]`) that "the perf layer may consume." This spec has no primitive for
any of it: no `$cue.*` context variable, no feature-space constraint key, no
rest-overlay anchor — and its live input vocabulary is `$conduct.*`
(fleet-jepa), a *different conductor* than the ensemble engine. As written, an
engine cue and a perf file cannot refer to each other at all. **Fix:** either
(a) add a cue context (`$cue.kind`, `$cue.payload.*`, published per cue fire)
plus a reserved constraint meta-key that `keep_empty` compiles into, or (b)
declare explicitly that cues are arrangement-level only and perf consumes only
conductor streams — but then engine §0.3's "that seam is the contract" needs
rewriting, because there is no seam.

### A3. [REFINED of §4.1/§11.1 — write-hostility] The anchor grammar is easiest for the machine and worst for the writer, and it is semantically wrong for drums.
§11.1's comping line enumerates eleven pitches (`a2-e3-c4-f2-a3-f4-c3-b3-d4-b2-d3`)
to mean "everything that isn't the melody" — information the compiler already
has. Meanwhile §4.1 addresses drums by *pitch* (`@drums a3 .last`), but the
evidence shows the drum map lives in a comment row (`@drums: C1 = kick feathered,
D2 = brush snare, A3 = ride barely there` — tap parts/drums.song line 1): the
pitch is an alias for an instrument, and the mapping is convention, not data.
Anchoring percussion by alias-in-a-comment is one rename away from silently
re-binding every drum annotation. **Fix:** (a) complement selectors (`* -
Melody`) so nobody enumerates chord tones by hand; (b) first-class
instrument-role targets for percussion voices (`@drums ride .last`), with the
drum-map comment promoted from convention to parseable row.

### A4. [NEW — seam] Feature-truth fork: perf mutates the features after the arrangement, and the engine's referee reads them before.
Perf changes what sounds — `vel:` expressions rewrite velocity_mean, thinned
comping changes note_density — but the engine (ADJUDICATE, `features_moved`
verification, SIMULATE's trace) computes features on the arrangement via
`analyze_features`. Once perf exists there are two feature truths: pre-perf
(what the referee scores) and post-perf (what anyone hears). Neither spec
acknowledges the fork. **Fix:** pick one and state it in both specs — either
adjudication runs on the post-perf trace (perf compiles before ADJUDICATE;
referee verdicts then match the room) or features are defined pre-perf and perf
is explicitly outside referee semantics. Do not leave this to implementation
accident; it decides whether "POCKET LOCKED" refers to the music or the map.

### A5. [REFINED of open question 5 — decide it now] Agents write `parts/*.perf` only; `[Perf]` sections are human-scale by construction.
The spec floats this as an open question, but the evidence already answers it:
ensemble agents write parts (every `write` in both session logs is a part
write); nothing suggests an agent needs in-score annotations. The 40-line
diagnostic (§5.1) only *warns after* a 400-line `[Perf]` section exists — in
session 2, that warning fires a hundred times and changes nothing. **Fix:**
close Q5 in the spec: `perf_write_part` accepts sidecar-style parts only, full
stop. Cheap, removes a merge-order ambiguity (§6's section-then-sidecar
collision case) for the entire agent population, and keeps `.song` human-scale
without enforcement theater.

**VERDICT: REVISE-THEN-SHIP.** The bones — anchor ledger/rebase, parked-never-
dropped, determinism harness, generated-ledger coordination — are the strongest
engineering in the three specs. Revise = one real cut (A1), two seam pins (A2,
A4), two grammar softenings (A3, A5). No rethink needed.

---

## B. ENSEMBLE ENGINE (`ensemble-engine-spec-draft.md`)

### B1. [NEW — the evidence's loudest lesson, missed] The obligations ledger notifies players who have left the room. There is no presence model.
The spec's founding defect — the ride-pull at 14 — was not a deadline failure.
Timeline from the log: drummer-glm's last write 16:20:18 (v6); the trade
*declared* 16:23:59 (v8, after the drummer was done); pianist enters 16:26:38;
the drummer never acts again. §3.4's fix — "the producer surfaces open
obligations at every round boundary" — assumes a round boundary and a present
producer relay reach a player who is, in fact, gone. Nobody was late; nobody
was there. An obligations ledger without a presence model is a notification
into the void, and session 2 will reproduce the exact defect with better
logging. **Fix:** obligations pair with chair presence — an obligation opened
against a departed/unheld chair triggers producer paging (re-invoke), a
renegotiation window, or an explicit decline-with-reason on the sheet; a
`leave` while obligations are open is a flagged event, not a silent exit.

### B2. [REFINED of §8.4 — the spec sees the disease, ships it anyway] `features_moved` mandatory-exactly-three without verification is ritual catnip.
The existing log summaries are already performative prose; LLM players asked to
"quote exactly three numbers that moved" will quote three beautiful numbers,
every time, forever. The spec's own countermeasure (compiler verification of
quotes against before/after) is deferred to v0.2 — meaning v0.1 *mandates the
ritual and builds the perception-coupling story on it*. **Fix:** invert the
v0.1 requirement: the compiler computes the top feature movers at write time
(it owns before/after — the hard part already exists), and the player's
mandatory field is *explaining* the compiler's top movers, not authoring their
own. Verified perception-coupling from day one; the "exactly three" quota goes
away entirely.

### B3. [NEW — overengineering] The reflex miner needs ≥3 sessions of support; the corpus has one interactive session. Don't build step 7 yet.
§6.1 gates proposals on support ≥ 3 sessions and consistency ≥ 0.7. The quilt
contains one multi-agent session (tap) and one solo take (duke-lab — no cues,
no trades, no other voices). MINE/PROPOSE/GATE/FIRE, trust-math hooks, reflex
demotion counters, and the §4 pipeline's simulate-reflex wiring are
infrastructure for evidence that does not exist. Building it now also forces
premature answers to Ship-of-Theseus (§8.2) and band-vs-player reflexes (§8.3)
— questions the data can't inform yet. **Fix:** v0.1 scope = sheets
(identity/defaults/refusals) + quilt nodes with edges + cue schema +
obligations ledger + retrieval onboarding + verified features. The miner
enters at v0.3, when three sessions of nodes exist to mine. This also shrinks
the trust-math problem (§8.5): with no trust-consuming consumers in v0.1,
"vibes" is temporarily acceptable.

### B4. [NEW — spec-lie adjacent] SIMULATE's "dead air" detector would have missed session 1's actual defect, and simulate ignores the perf layer.
§4.6 and §7 claim unresolved cues "surface as dead air — a hole at 14.1 …
which is literally what session 1's score contains today." It doesn't. The
shipped drums part bar 14 is `a3 d2 a3 d2` — the ride *keeps playing*; the
defect is texture that never cleared, not absence. A dead-air detector watches
for the wrong signature of the spec's own canonical failure. Separately,
SIMULATE renders "the arrangement + feature trace" via plainsong — no perf
compile — so the preview of "what the band would play" has no touch, while the
band's actual output (post-perf) would score differently (see A4). **Fix:**
detect obligation-*implied feature deltas* (did drums density drop at 14 as the
trade's ride-pull implied? no → flag), and define simulate's relationship to
perf (compile it, or declare the preview touch-less and the referee
pre-perf — same decision as A4, made once).

### B5. [NEW — spec-lie] "These exist as working behavior already" overstates the Kestrel — and §7 contradicts the log.
§1.2 presents all four personas as working behavior, including "The Kestrel —
three readings of the same settled changes: smoke / ballad / foghorn-kestrel."
The log shows *one* reading (v12, 16:36:52: "smoke reading in my own styling").
§7 then calls tap:v12 "would-be … not yet played." Both cannot be right, and
neither is: v12 exists and is the smoke reading; ballad and foghorn were never
played. Small, but this is the evidence-inflation pattern — and yard-band's
lineage table already inherits "three readings" as established fact. **Fix:**
state it as one-of-three demonstrated, two-aspirational. Personas seeded by one
session are hypotheses; the spec's own §1.3 ("a sheet with no provenance is a
costume") is the standard — apply it to the seed paragraph too.

**VERDICT: REVISE-THEN-SHIP** — the lightest lift of the three. B1 and B2 are
the load-bearing revisions; B3 is scope discipline; B4/B5 are honesty fixes.
The cue schema, quilt-node shape, and retrieval onboarding are right.

---

## C. YARD BAND (`yard-band-spec-draft.md`)

### C1. [NEW — spec-lie in the lineage table] The clock has no lineage. Appendix C claims a pattern that does not exist.
Appendix C: "Tick → cascade → tape → WS broadcast — YardRoom pattern, verbatim
shape." I read `src/room.ts`: the YardRoom **ingests external `POST /tick` at
2 Hz** ("ingests ticks from…" — line 2; TAPE_MAX sized "~4 min at 2 Hz"). There
is no self-scheduling DO alarm anywhere in the fleet. The one mechanism the
entire design hangs on — a self-rescheduling 625 ms DO alarm running for hours
(§2.1) — is genuinely new, unproven, and presented as sibling-pattern reuse.
§13.1 flags "alarm floor" as an open question, which understates it: the
question is not whether the alarm is reliable enough, it's that this clock
architecture has never run anywhere. **Fix:** promote to first-class risk with
a designed fallback (dedicated ticker worker / external metronome service
POSTing ticks — i.e., the pattern that *does* exist — with the DO as
truth-owner and catch-up loop unchanged), and correct Appendix C. The catch-up
loop design is good; the claim of lineage is not.

### C2. [NEW — critical path mis-ordered] The streaming partial-commit assumption is the spine, is unevidenced, and the tier table contradicts all observed latency.
Every observed agent write in the corpus is batch: tap writes 64–155 s; duke-lab
117 s to first write. The T0 row's "8–40 s" is supported by nothing. At 40 s,
H = 16–24 bars > H_max = 8 even before streaming questions — meaning the
"section planner" role at 96 bpm only works *if* streaming lands, and the
`/ask` lanes are Workers AI reasoners (`chat.ts` notes flash "spends tokens on
reasoning_content" before any output — reasoning tokens delay first parseable
bar beyond naive TTFT). §13.3 lists this as open question 3; it is not an open
question, it is the go/no-go for the headline feature. **Fix:** reorder — the
streaming spike runs *before implementation step 1*, not alongside step 4;
relabel the §3.1 table "provisional, pending spike"; and design T0's honest
role as **between-tune planner** (BETWEEN state, no deadline pressure), with
T1 as the only in-flight thinking lane. If the spike fails, the spec still
stands — as a reflex-tier band with slow-lane setlists — but say so now.

### C3. [NEW — spec bug] "Humans are never optimized" is violated by composition.
§7.3.6: humans never feed parameter updates. §8.1: bandit reward
r = ΔC_plan_adjusted + 0.3·F. §7.1: C includes S_cue = executed/due, **two-
sided** — the guest's side of a trade4 counts as due. §11.2's own worked
example: guest plays nothing → "hole marked, zero punishment" — trust is
untouched, but S_cue(29–32) < 1 drags C down, the bandit updates the *band's*
knobs on the guest's absence, and §11.2's last line even says the bandit moves
"toward the guest's observed fit." A kid who freezes during their solo
silently retrains the band around their absence. Directionally opposite to the
design's own doctrine. **Fix:** one line — `C_bandit` scores robot-side
obligations only; `C_display` keeps the full room. The guest teaches by
playing, never by failing to.

### C4. [NEW — seam] "Ensemble schema, verbatim" is false three ways, and the divergences corrupt exactly the cross-session mining that justifies the schema sharing.
(a) *Enums:* ensemble has 5 cue kinds; yard has 8 (`nod`, `grin`, `trade4`
added, `landing`→`land`). (b) *Units:* ensemble `t_minus` is always beats
(§3.1); yard's is beats for intra-bar kinds and **bars** for structural kinds —
a `trade4` with `t_minus: 8` means 8 bars = 32 beats; projected onto the
ensemble schema un-mapped, its meaning shifts 4×, and §6.1's miner
pattern-matches on "t_minus band" — the mined reflex will be wrong by a factor
of four. (c) *Obligation lifecycle:* yard obligations die at freeze
(`broken-by-deadline`), ensemble obligations live until diffs appear —
projection must map statuses or history lies. Same for `band_sheets` =
"ensemble §1 schema, verbatim": knobs/tier/horizon/misses have no home in that
schema (they're room cells in §4.1 — so they die with the room, and the
bandit's learned knobs never persist to the player). **Fix:** this spec is the
consumer, so this spec owns the mapping table (kind, unit, status, sheet-
overlay — a `live:` extension on ensemble sheets). Drop the word "verbatim"
everywhere it currently appears; it's doing the opposite of its job.

### C5. [REFINED of §7.3/§8.1 — overengineering] The Goodhart apparatus is sized for a research program; the data is an evening.
Holdout C′ with rotated jittered weights, skip-flagged bandit updates,
Thompson sampling over a 10-scalar knob vector — for ~5–10 between-tune
updates per session on 64–256 bars, which the spec itself says can only "move
scalars." The formulas (C, F) are good and should ship as *taped metrics*; the
bandit-plus-holdout machinery is disproportionate and will mostly consume
producer attention. **Fix:** v0.1 = C/F computed and displayed (kids' HUD,
Wreck Reels, tape) + naive per-knob EMA toward observed fit; the bandit and
holdout return when ≥10 sessions exist. Keep §7.3.1–7.3.4 (server-only,
producer-locked plans, saturation, two-sided cues) — those are cheap and real;
cut §7.3.5 and §8.1's sampler until there is a bandit worth guarding.

**VERDICT: REVISE-THEN-SHIP — with a hard gate.** The freeze seam, write-ahead
buffer, transforms-at-freeze, and "the hole sounds but can't happen invisibly"
are the best architecture thinking in the seminar — collapse-of-two-times is
the right thesis. But two claims are currently false (C1's lineage, C2's tier
table) and one guardrail is self-violating (C3). Gate the ship on: streaming
spike results (C2), clock fallback designed and soak-tested (C1), and the
C_bandit split (C3). If the streaming spike fails *and* the alarm soak fails,
the live-twin thesis downgrades to RETHINK — the band becomes a reflex-tier
puppet show with a nice quilt view.

---

## Cross-cutting coda (not counted in any spec's five)

The three specs cite each other as load-bearing in their most speculative
places: perf's ensemble integration (§11.8) assumes engine ownership rules that
are a draft; the engine's §0.3 seam assumes a perf spec section that doesn't
exist (A2); yard-band consumes ensemble §1/§6 "verbatim" while diverging from
both (C4). This is a circular dependency of unshipped specs — each treats the
other's TBD as settled. One afternoon of seam-pinning (A2, A4, C4's mapping
table, one decision on agent containers A5) collapses the circle into a chain.
Do that before any implementation order list executes.

And a note for the record: the task brief cited `duke-lab/REPORT.md` as
evidence; no such file exists. The specs' fondness for slightly-enhanced
evidence (B5, C1) starts at the seminar's own intake. Worth fixing the habit at
the source.
