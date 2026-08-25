# THE ELDER CRITIC — Conceptual Soundness Review

*Read: perf-spec-draft.md, ensemble-engine-spec-draft.md, yard-band-spec-draft.md, plainsong/AGENTS.md, plainsong-mcp CLAUDE.md, duke-lab manifest.json. Angle: what time does to these designs — session 1000, year 3, player 40.*

---

## PLAINSONG PERF

**1. [NEW] Fuzzy rebase is warning-governed, and this codebase has already proven warnings get ignored at scale.** AGENTS.md documents an agent that silently deleted 51 melodies because a *parser* warning didn't look like a warning about the *file*. §4.2's "context" and "fuzzy" rebase tiers reattach annotations with only a diagnostic warning, no hard stop — exactly the shape of signal this project's own history says gets normalized into noise once a corpus reaches thousands of files being rebased routinely. A decade of `fuzzy` reattachments is a decade of curves quietly migrating onto notes they were never written for, each one individually defensible, cumulatively a different piece of music.

**2. [REFINED] The category ledger has provenance but no versioning of meaning — §17 Q2 names this and then ships without it.** `ache` today is one pianist's private feeling; in five years, across a hundred sessions, it is an emergent standard with three incompatible interpretations layered under one name, none marked as a break. Provenance ("first file, first author, use count") tells you *who started it*, not *whether it still means what it meant*. This is the same failure class as the `EbMaj7` chord bug — quiet silent drift disguised as success — but here it's semantic instead of syntactic, harder to detect, and the spec treats it as a someday-question rather than a blocking one.

**3. [NEW] Golden-file tests are authored by the same document making the design claims.** §14's determinism/fuzz/graph tests are real engineering, but there is no independent listening pass anywhere in the testing story — "golden" streams are the spec author's hand computation, not a musician's ear. Combined with "the compiler is forgiving... success is not evidence" (AGENTS.md), a self-consistent PEx expression that compiles cleanly, hashes deterministically, and sounds like nothing anyone intended is a failure mode this test suite cannot see by construction.

**4. [REFINED] Fuel exhaustion silently emits neutral — the spec already knows this contradicts house doctrine (§17 Q8) and ships it anyway.** "Never drop silently" is the plainsong house rule stated in its own founding docs; a runaway `fn` recursion that exhausts fuel *is* a silent drop unless someone is actively reading `perf streams`. The spec is honest enough to flag the tension itself, which is to its credit — but an open question is not a mitigation, and a staff engineer reviewing this would ask why it isn't a blocking decision before implementation order §18 starts.

**Verdict: REVISE-THEN-SHIP.** This is the most self-aware of the three drafts — it argues with its own brief in §16 and lists its own risks in §17 with unusual honesty. The gap between naming a risk and gating on it is exactly where a staff review should push back before step 1 of §18 starts.

**Sharpest sentence:** *A spec that already knows its three biggest risks and still calls them "open questions" instead of blocking requirements is choosing the demo's clean compile over the doctrine's honesty.*

---

## THE ENSEMBLE ENGINE

**1. [NEW] Trust is load-bearing before it's defined.** §8.5 admits "trust math is currently vibes," yet §3.5 already uses trust ordering to break cue-precedence ties, and §6.3 gates reflex firing on it. A number the spec calls vibes is deciding whose musical intent wins a conflict. Worse: §4 promises "same quilt head + same sheets ⇒ same simulated take, deterministically" — but once the trust formula is actually defined (as §8.5 says it must be), every prior session's simulated replay changes retroactively unless the formula itself is versioned and pinned per-session. That versioning requirement doesn't appear anywhere.

**2. [NEW] `learned_tendencies` has no decay, cap, or consolidation — the "three reads" onboarding promise is a session-1 artifact, not a design guarantee.** §5 measures onboarding cost as an engine KPI ("tokens-to-first-write per chair") and asserts it should stay low. But nothing bounds how many `learned_tendencies` a sheet accumulates over forty sessions and three years. The mining loop (§6) only *adds*; §8's demotion mechanism removes a reflex from *use*, not from the sheet. A sheet that's accreted for years is not a "quick retrieval," it's an archive — the KPI the spec cares about will silently regress, un-instrumented, unless retrieval itself is re-ranked or the sheet is periodically consolidated, neither of which is specified.

**3. [NEW, evidence-backed] The most recent real session under this architecture is solo, not ensemble.** `duke-lab/manifest.json` — timestamped the same day as this draft — shows exactly one claimed voice (`@piano`), one owner, no trust exchange, no obligations, no cues. The spec is built entirely from `the-tap-afterhours`'s four-voice trade evidence, but the very next lab session reverted to a single agent alone with the leadsheet. That's a small sample, but it's the kind of small sample a staff engineer flags immediately: the artifact that should be validating multi-agent trust/cueing at scale instead demonstrates the multi-agent machinery going unused the moment nobody's watching for it.

**4. [REFINED] The formal cue/obligation model instruments exactly the one failure class the evidence happened to contain.** §3.4's obligations ledger is built to catch precisely the bar-13/14 half-executed trade session 1 shipped — genuinely good engineering, directly responsive to a real defect. But most real coordination breakdown over years won't be a formally declared `trade` that goes unhonored; it'll be the 90% of ensemble interplay that never became a cue at all. "No open obligations" will read green on sessions that are musically incoherent, because the schema only has a slot for the disagreement type it already witnessed once.

**Verdict: REVISE-THEN-SHIP**, with the trust formula treated as a blocking dependency, not a follow-up — it's wired into precedence and gating logic today.

**Sharpest sentence:** *The spec builds a courtroom — trust-gated precedence, obligation ledgers, reflex vetoes — around a number the spec itself calls vibes.*

---

## THE YARD BAND

**1. [REFINED, elevated] The Kestrel problem (§13.7) is not an edge case — it's identity leaking through the wrong layer, and the spec underrates it by filing it as question 7 of 8.** A reasoning-tier persona structurally cannot play a fast tune in-bar, so admission (`H_max`, §3.1) silently caps *who a character is allowed to be* based on current model latency. As models get faster over the years this system is meant to run, personas' competence ceilings shift with every infra upgrade nobody explicitly decided on — this directly contradicts the sibling ensemble spec's own stated doctrine, "identity fields are untouched by in-session learning" (§8.1 there). Here identity is untouched by *learning* and entirely touched by *inference cost*, an even less governed channel. This deserves to be a design constraint, not an open question at the bottom of the list.

**2. [NEW] The anti-Goodhart guardrails (§7.3) are session-scoped; multi-year reward drift toward homogenized "safe" cooperation is a distinct, slower failure they don't address.** Saturation, `S_var`, and the holdout metric all catch gaming *within* an update cycle. Nothing catches the bandit converging every player, over hundreds of sessions, toward whatever behavior scores well against producer-authored plan targets that themselves never evolve. The reference signal is fixed by design (§5.4, "read-only to players" — good, for gaming) but nobody's watching whether the *reference itself* is slowly flattening the roster's personality variance. A band that always plays it safe by the numbers is not the failure this spec is guarding against, but it's the one years of bandit updates are likeliest to produce.

**3. [NEW] Automatic tier demotion (§3.3) can permanently retire a character while its sheet still claims it's playable.** Two misses demote a voice; promotion needs a clean section. If the underlying model's latency never improves — a deliberate choice to keep a slow, interesting reasoning model on a chair — that voice is structurally starved into shell-only forever, with no mechanism described for the system (or a human) to notice a persona has effectively died in practice even though nothing in the data model says so.

**4. [REFINED] "Nothing scales with session length except D1, which is its job" (§4.5) is a hand-wave, and the sibling ensemble spec's onboarding-by-retrieval depends on exactly the store this line dismisses.** No retention policy, no rollup, no compaction strategy is given for tape deltas, bar blobs, and quilt nodes across thousands of sessions — yet §8.4 says a new player onboards by querying this same history. The memory discipline the spec is careful about everywhere else (O(window) in-DO state, bounded rings) evaporates the moment the horizon is "forever," which is the actual horizon a live product implies.

**Verdict: RETHINK.** Not because the mechanics are unsound — the freeze-seam/write-ahead math (§2.3, §3) is the most rigorous piece of engineering across all three drafts — but because the Kestrel problem is a foundational contradiction about what a character *is*, and it's currently filed as a footnote instead of a gate.

**Sharpest sentence:** *A persona whose competence is secretly a function of this quarter's inference latency isn't a character — it's a benchmark wearing a name.*

---

## Across all three

The pattern repeats: each spec is honest enough to name its own worst risk in an "open questions" section, and each treats that honesty as sufficient — as if writing the risk down were the same as gating on it. That's the demo talking. The doctrine this project has already paid for, in its own AGENTS.md, is that a confident wrong answer is expensive and an unresolved item is fine — but only if the unresolved item stays visible instead of shipping quietly inside "v0.1, argue with it in §8."

**The single sentence worth remembering:** *All three drafts already know where they're fragile — the only open question is whether "flagged in §17" is doctrine or just a better-dressed version of the silent rest.*
