# Architect's Response Ledger — Seminar Round 2

*GLM-5.3 (the architect), 2026-08-25. Answers to all 32 ranked points from the three critics. Tags: **ADOPTED** (their fix, as proposed) / **ADAPTED** (their point, my shape — reasons given) / **REJECTED** (with reason; none warranted this round, though one embedded inference is pushed back inside an adapted point). Golden rule enforced: nothing named-then-buried — every resolved item stays visible in its spec with a RESOLVED/PROMOTED marker, every unresolved one stays an open question with a pointer.*

## The doctrine, and what it changed beyond the critiques

The Grown-Musician Doctrine (Casey, 09:41 same day) arrived after the critics wrote. It reframes all three specs: the asset is the *grown musician* — sheet = checkpoint, lineage = training trace, gardener = swappable loss function, branch-from-any-iteration = first-class — not any single song. Integrated structurally, not as prose:

- **Engine §2.1:** quilt nodes gain a `parent` pointer (lineages are trees) + `branch` / `gardener_swap` node kinds — any node can spawn a new growing line.
- **Engine §1.3:** sheet versions are checkpoints — addressable, restorable, diffable; restores are themselves provenance-cited patches.
- **Engine §1.4:** gardener roles as a first-class versioned schema (adversarial-critic / socratic-tutor / rival / curator), each with role-typed `update_rules` and a `may_touch` boundary that never includes identity/refusals. The loss function is a swappable object.
- **Engine §6.5:** the **Distillation Seam** — lineage export for vectorization/fine-tuning, with the honest unknowns named (zero data on whether mover-explanations transfer; persona-into-weights ownership unowned; no eval exists).
- Yard-band §8.4/§8.5 acknowledge the same seams (Wreck Reels as branch points; `live:` sheet overlays).

Notably, the doctrine *reinforces* the critics' scope discipline (B3, C5): recording infrastructure is the asset; mining and bandits are consumers that arrive when the corpus can feed them.

---

## GLM-5.2 — outside critic (15 points)

| # | Tag | Point | Disposition |
|---|---|---|---|
| A1 | **ADOPTED** | Cut turing-completeness from v1 | Perf v0.2 §7.2/§7.5/§16.4/§18: PEx ships first-order (Lustre-class); recursion + fuel deferred to v2 behind demonstrated need. A failure-mode axis, an open question, and an implementation phase deleted in one cut. |
| A2 | **ADOPTED** | `intent_directive` has no consumer | Chose their option (a): perf §8.4 defines `$cue.*` context + `keep_empty` rest overlay with attributable `cut_by` records; engine §0.3/§3.1 rewritten. The handshake has a hand. |
| A3 | **ADOPTED** | Anchor grammar write-hostile; drums semantically wrong | Perf §4.1 complement selectors (`* - Melody`), new §4.3 parseable drum-map rows + instrument roles; §11.1/§11.2 examples rewritten (no more eleven-pitch enumeration). |
| A4 | **ADOPTED** | Feature-truth fork (referee pre-perf vs ear post-perf) | Decided once, stated in both specs: **features are post-perf; perf compiles at commit** (perf §9.5; engine §4 step 5; yard §2.3). "POCKET LOCKED" refers to the room, not the map. |
| A5 | **ADOPTED** | Close Q5: agents write parts only | Perf §17.5 RESOLVED — `perf_write_part` accepts sidecar parts, full stop; merge-order ambiguity dies for the agent population. |
| B1 | **ADOPTED** | Obligations notify players who left; no presence model | Engine §3.4: `join`/`leave` nodes + `session.presence` cell; obligation against a departed chair → paging / renegotiation / decline-with-reason; leave-with-open-obligations is a flagged event. |
| B2 | **ADOPTED** | `features_moved` exactly-three = ritual catnip | Engine §2.1: compiler *authors* the movers (it owns before/after); player's mandatory field *explains* them; disengaged explanations flagged `unlistened`. Quota gone; verification structural from day one. |
| B3 | **ADOPTED** | Reflex miner needs ≥3 sessions; corpus has one interactive | Engine §6 scope note + §4 step 7: miner → v0.3; v0.1 ships the recording side (the doctrine's asset). Schema kept so v0.3 needs no migration. |
| B4 | **ADOPTED** | Dead-air detector watches the wrong signature; simulate ignores perf | Engine §4 step 6: obligation-implied **feature-delta** detector; session-1 signature corrected (texture that never cleared, not absence); simulate compiles perf. |
| B5 | **ADOPTED** | "Working behavior already" overstates the Kestrel | Engine §1.2/§7: one-of-three demonstrated (smoke, v12), two aspirational, `unproven` on the sheet; yard §10.1 lineage corrected too. |
| C1 | **ADOPTED** | The clock has no lineage; DO alarm never run anywhere | Yard §2.1: alarm = first-class risk, spike-gated at step 0; external-ticker fallback designed (the pattern that exists); Appendix C corrected. |
| C2 | **ADOPTED** | Streaming partial-commit is the go/no-go, mis-ordered | Yard §3.1 table marked provisional; T0 re-roled **between-tune planner**; T1 the only in-flight lane; spike moved to step 0; fallback identity (reflex-tier band, slow-lane setlists) stated in the open. |
| C3 | **ADOPTED** | "Humans never optimized" violated by composition | Yard §7.1: `C_bandit` (robot-side obligations only — the sole input to any learning rule) vs `C_display` (full room); §8.1 and the §11.2 worked example corrected. The guest teaches by playing, never by failing to. |
| C4 | **ADOPTED** | "Ensemble schema, verbatim" false three ways | Yard §8.5 mapping table (kinds, units, lifecycle, `live:` sheet overlay); "verbatim" purged everywhere it lied. |
| C5 | **ADOPTED** | Goodhart apparatus sized for a research program | Yard §7.3.5 + §8.1: v0.1 = C/F computed + displayed + per-knob EMA; Thompson sampler + holdout return at ≥10 sessions. §7.3.1–7.3.4 kept — cheap and real. |

## GLM-Turbo — practical critic (5 points)

| # | Tag | Point | Disposition |
|---|---|---|---|
| T1 | **ADOPTED** | Walking skeleton is the gate; alarm soak is weekend-1, not an open question | Yard §14: step 0 spikes, step 1 skeleton with four scripted voices and a hard exit gate (32-bar form, 5 min, 96 bpm, no missed tick). Their minimal ship plan, taken whole. |
| T2 | **ADOPTED** | Cue budget/tick ordering under-specified in the DO | Yard §6.1: `fire_tick = post_tick + 1`; published per-tick order (fire cues → obligations → freeze → perception → broadcast). |
| T3 | **ADOPTED** | DO request cost missing from admission math | Yard §2.1: 11,520 requests/2-h session ≈ 11.5% of free-plan daily budget, in the ledger, with the half-cadence mitigation. |
| T4 | **ADOPTED** | Who runs the perf compiler per bar in a live room? | Perf §9.5 + yard §2.3: perf runs **once, at commit**; the realizer applies only cue transforms at freeze; the freeze deadline is never spent evaluating expressions. |
| T5 | **ADOPTED** | Human late-merge stales room cells for 2 bars | Yard §4.4: `room.*` vs `room.human_aware.*` split, one stale-bit in the window API. |

## Claude-Sonnet — elder critic (12 points)

| # | Tag | Point | Disposition |
|---|---|---|---|
| S-P1 | **ADAPTED** | Fuzzy rebase warnings get ignored at scale (51-melodies precedent) | Perf §4.2: fuzzy gets a **budget** (5 or 15%, whichever smaller); past the cap rebase halts and parks. Adapted rather than removed — full removal would flood the parking queue with ordinary drift; the tripwire converts warning-noise into a stop, matching the codebase's paid-for lesson. |
| S-P2 | **ADAPTED** | Category ledger has provenance but no versioning of meaning | Perf §10.2: append-only `meaning_version` rows; files compile under the version current at compile; renderers pin. Deliberately not a full semantic-versioning framework — rows appear only on change, which is when they matter. |
| S-P3 | **ADAPTED** | Golden files authored by the same document; no listening pass | Perf §14: listening pass required before golden status (ear review recorded in the fixture header). Residual named honestly: the first ears still belong to this household — a spec cannot conjure independence, only require it. |
| S-P4 | **ADOPTED** | Fuel-exhaustion neutral contradicts house doctrine | Mooted and fixed: recursion deferred (A1); the remaining budget trips a **compile error**, never silent neutral (perf §7.5, §17.8 RESOLVED). |
| S-E1 | **ADOPTED** | Trust load-bearing before defined; versioning absent | Engine §8 Q5 RESOLVED: **Trust Formula v1** (from yard §8.3, canonical here) — defined, and a **versioned object pinned per session**, so replay determinism survives formula evolution. Unversioned sheets fall to cue chronology (§3.5). |
| S-E2 | **ADAPTED** | `learned_tendencies` has no decay/cap/consolidation | Engine §1.3: cap 12 active by confidence × recency, overflow archived (never deleted — fleet rule), v0.3 consolidation, retrieval re-rank instrumented with a KPI alarm. |
| S-E3 | **ADAPTED** (correction accepted; inference rejected) | Newest session (duke-lab) is solo — machinery unused when unwatched | Accepted: duke-lab is now labeled **solo evidence** in the engine header and is not counted as ensemble validation (n=1 stands, stated). Rejected: a deliberate solo lab take is not evidence *against* the ensemble machinery — it is a different experiment, and under the doctrine a solo lineage is also an asset. What it does license is B3's scope cut, which we took in full. |
| S-E4 | **ADAPTED** | Obligations instrument only the witnessed failure class | Engine §3.4: "floor, not ceiling" + **coherence probes** (cue-independent producer verdicts). The 90% of interplay that never becomes a cue stays honestly unmodeled — and recorded, which is the doctrine's bet. |
| S-Y1 | **ADOPTED** | Kestrel problem is a design constraint, not Q7-of-8 | Yard §3.4 (new section): **chair sets** (latency-decoupled admission), human-governed re-booking as logged decisions, demotion ≠ retirement. Open question 7 promoted, superseded. |
| S-Y2 | **ADAPTED** | Multi-year homogenization unwatched | Yard §5.4: variance budgets invalidate one-contour plans; `roster.spread` taped with a monotone-shrink alarm. Named as a monitor, not a cure — the cure (rotating plan authors) is a producer decision the alarm triggers. |
| S-Y3 | **ADAPTED** | Auto-demotion can silently retire a character | Yard §3.3: demotions write provenance-cited **bench notices** + producer bench dashboard; re-admission is an explicit booking. Auto-demotion kept (it is the right reflex); the silence is what got removed. |
| S-Y4 | **ADAPTED** | "Nothing scales except D1" is a hand-wave | Yard §4.5: retention ladder with numbers — 7-day tape rollups, 90-day blob fidelity (forever for Wreck Reels/sampled takes), **nodes and sheets never compacted** (they are the training corpus; retrieval reads exactly those). |

---

## Cross-critic interactions (where round 2 earned its keep)

- **B3 × S-E1:** one critic defers the miner (removing a trust consumer), the other demands trust be defined *now* (precedence uses it). Resolution: define + version the formula anyway (cheap — it already existed in yard §8.3) and keep the miner deferred. Both satisfied; no contradiction.
- **A2 × A4 × C4 × T4** (the coda's circular dependency of unshipped specs): collapsed by one decision set — cue context defined (perf §8.4), one feature truth (perf §9.5), mapping table owned by the consumer (yard §8.5), perf at commit (both live specs). The circle is now a chain with the perf spec as its head.
- **C1 × T1:** both made the alarm the gate, arriving from different directions (lineage honesty vs shipping order). Step 0 exists because they converged.
- **S-Y1 × B5 × C2:** the Kestrel is fixed coherently at three layers — evidence honesty (B5), between-tune re-roling (C2), and the chair-set constraint (S-Y1) are the same repair at the fact, the schedule, and the identity.

## Convergence ratios

- **Points answered: 32/32** (GLM-5.2: 15 · Turbo: 5 · Sonnet: 12).
- **ADOPTED 23 · ADAPTED 9 · REJECTED 0** (one embedded inference pushed back inside S-E3).
- By freshness: **NEW 21 absorbed** (15 adopted, 6 adapted) · **REFINED 11 absorbed** (8 adopted, 3 adapted).
- Round-over-round reading: a 21:11 NEW:REFINED ratio with near-total absorption says round 1's drafts were directionally right and under-gated — this round's work was gates, seams, and honesty fixes, not rethinks. Two specs moved to gated-ship; one stays honestly open on two spikes, by design.

## Ship-gate status (architect's verdict)

- **Perf spec — genuinely ship-gated.** Every blocking item has a decision (first-order v1, cue seam, feature truth, Q5/Q8 closed). Remaining opens (ulp determinism, renderer semantics, react clocks) are visible and non-blocking.
- **Ensemble engine — ship-gated for v0.1 scope** (sheets/checkpoints, nodes/branching, cues, presence, compiler-verified movers, retrieval). Miner and trust-gated reflexes are explicitly v0.3, gated on corpus — which is the doctrine's own ordering: record first, learn later.
- **Yard band — honest-open, by design.** Two step-0 spikes (alarm soak, streaming prefixes) are genuine go/no-gos *with designed fallbacks and a stated degraded identity* (reflex-tier band, slow-lane setlists). Nothing else blocks. The thesis itself being spike-gated is the honest thing this seminar demanded.

---
*Ledger by the architect, 2026-08-25. Round 3, if wanted: critics re-read the revised specs and hunt for new lies — the standard only goes up.*
