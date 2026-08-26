# Reflex Mining Report — Candidate Reflex Registry

*The Ideation Lane, 2026-08-25. Mined: 6 ensemble session logs + BUILD-JOURNAL.md, 10-stitch stitch-log.jsonl + GATE1-REPORT.md, 3 cross-model seminar critiques + architect response, cell-cascade seed.json + v0.2 verification. Cross-checked against the 4 seeded organisms so everything below is NEW.*

**Method note (honest, per house rule):** the seed set already carries — Duke's musical tendencies (Vel rows, displacement, contour rotation), band-clock absolute deadlines, cue-tokens prefix-law acks (incl. WILCO repeat-back parity), seamstress-eye one-directional-point method. Everything below extends beyond those or names a different layer.

---

## PART 1 — TOP 5 NEW REFLEX CANDIDATES

### 1. SACRED-SPACE-HONOR *(strongest signal in the corpus)*
**Statement:** When one player explicitly declares a space empty ("bar 9 is yours," "no fill over the final root"), every later entrant honors it — entering that space at all requires asking permission, and the ask is a question, not an assumption.

**Evidence (6 decisions by 4 independent agents, zero violations, one permission-ask):**
- Bassist declares: "bar 9 I drop out after beat 2 — leave that bar almost empty... breathe around bar 16 — I land long and low on the root, let it ring, no fill over it" (BUILD-JOURNAL, TO THE DRUMMER)
- Drummer honors + re-declares: "Bar 16 is yours — kick on your root, ride letting ring, no fill, I promise"; bar 9 "just ride on 1, one brush swirl on 3, nothing else" (BUILD-JOURNAL, DRUMMER->BASSIST)
- Pianist honors: "Sacred spaces kept: bar 9 only one held a3-e4 on beat 3; bar 16 silent over the long root" — and **asks**: "if you want bar 9 completely naked, say so and I'll lift it" (BUILD-JOURNAL, piano)
- Vocalist honors the space *and* the pianist's floor: "Bar 9: silent first half — one word 'home' on E4 landing inside the pianist's beat-3 dyad"; answers the question: "keep the dyad — floored, not naked" (BUILD-JOURNAL, vocal chair)
- log.jsonl corroboration: drummer "bar 9 left open for the bassist" (v5), "no fill over bar 16" (v6)

**Observed count:** 6 (4 agents, 16 bars — every declared space held)
**Proposed tier:** **cue-reflex (sclerotic)** — the trigger is a formal declarative act, the response is deterministic: declared-space ⇒ stay out or ask. No model call needed at fire time.
**Distills into:** `cue-tokens` organism, new `space-ledger` cell beside `cue-ack` — a `declare-space` cue kind with rules {stay-out, ask-before-enter, honored-by default}. Mirror at the music layer of the STANDBY/keep_empty seam the seminar pinned (perf §8.4).

---

### 2. HONEST-GAP-DECLARATION
**Statement:** When a capability is structurally unavailable or convergence hasn't happened, say so in the artifact itself — never simulate past it. "INEXPRESSIBLE" and "not CONVERGED" are written into the journal, not smoothed over.

**Evidence (8 instances, 5 independent contexts):**
- Duke R2: "INEXPRESSIBLE from the voice: intra-bar per-note dynamics and swing... HONEST GAP declared: not CONVERGED; best take = version 4" (BUILD-JOURNAL)
- Duke R4: "syncopation requires a specific attack pattern I cannot reliably reproduce by intuition... Stopping here — 4 rounds, the gains are diminishing" (BUILD-JOURNAL, ROUND 4)
- Seamstress GATE1 honesty ledger: "The grower did not 'learn.'... The eye is a function, not a model... The plateau is real" (GATE1-REPORT.md — three named limits in one document)
- GLM-5.2 critic catches the anti-pattern: B5 "three readings" claimed, one played → architect fixes to "one-of-three demonstrated, two-aspirational, `unproven` on the sheet" (seminar-critique-glm52.md §B5, seminar-response.md)
- Cell-cascade v0.2 itself: boundary answers "model-call-required — the boundary stays honest"; rule-miss is scar tissue, "not silent guessing"; `cost_estimate_usd: null` "honest: tokens logged, cost not guessed" (v0.2-live-verification.md)

**Observed count:** 8+
**Proposed tier:** **rule (differentiated)** — mechanically checkable at write time: any convergence claim, capability claim, or artifact citation must be resolvable (artifact exists, count demonstrated vs aspirational split). Misses escalate to the germ line for judgment.
**Distills into:** new `honesty-gate` cell in a `fleet-ensign` organism (or hung off `seamstress-eye`, whose sheet already carries an `honesty` key — this makes it a live check instead of a self-description).

---

### 3. ROOM-FLOOR-CALIBRATION *(velocity under the room's mean)*
**Statement:** A late entrant reads the room's established dynamic floor and enters at or below it — the room's accumulated quiet is a floor the entrant must not break; register and placement sit *under* what's already playing.

**Evidence (4 calibrations, each strictly descending):**
- Bass establishes vel 66, behind the beat (BUILD-JOURNAL)
- Drummer enters: brushes vel 46, kick "feathered," ride "barely there" (BUILD-JOURNAL, log v5: "ride barely th...")
- Pianist enters: shells vel 52, register parked e3-a3-c4 under the vocal's future space (BUILD-JOURNAL, log v10)
- Vocalist, offered three lab readings (smoke 72-88 projected), declines all three: "the room had already decided it (bass vel 66 behind the beat, brushes 46, piano shells 52; anything projected would have broken the floor the rhythm section spent the whole conversation laying)" — enters sitting under the piano shells, entries behind the beat (BUILD-JOURNAL, vocal chair)
- Same shape, declined loudly: bassist rejects the counter-deal because "pushing against a feathered brush ride at 96 would stick out of a line that sits behind the beat everywhere else" (BUILD-JOURNAL, bass v8)

**Observed count:** 5 (4 entries + 1 refusal-for-consistency)
**Proposed tier:** **rule (differentiated)** — computable from the room state at join time: entry vel ≤ established mean, entry register outside occupied tessitura. The perception tools already measure exactly this (velocity_mean per voice).
**Distills into:** new `room-entry` cell — a differentiated player-cell rule evaluated at `join`/first-write, fed by `perception_trace`. Natural sibling to the band-clock's commit rule: clock checks *when*, this checks *how loud*.

---

### 4. CRITIQUE-BUDGET-LAW *(one concrete ask per iteration — fleet-wide)*
**Statement:** Every critique arrives bounded and ranked: one point when steering a growth loop, ≤3–5 ranked when reviewing a spec. Never a laundry list; never vague. (The seed has this as the *eye's* method; the corpus shows it is a *fleet-wide* conversational law, practiced by every model that ever took the critic chair.)

**Evidence (15+ bounded critiques across 4 models):**
- Seamstress eye: "ONE POINT" in every one of 10 stitch critiques, each naming the largest normalized gap in feature language (stitch-log.jsonl, all 10 rows)
- Grower obeys the receiving side: "Each stitch it hears ONE point of critique and deepens ONE layer" (GATE1-REPORT.md)
- Duke blind critic: exactly 3 ranked points per round, 3 rounds (BUILD-JOURNAL, R2 revision "per critic, 3 points"; HARSH CRITIC PASS 2)
- GLM-5.2 seminar protocol: "max 5 points per spec, ranked, tagged NEW or REFINED, each directional" (seminar-critique-glm52.md header)
- Turbo: shrinks its own critique to a minimal ship plan — "Shrink §14 step 1 to *exactly this*" (seminar-critique-turbo.md §1)
- Architect closes the loop with the verification half (B2 ADOPTED): compiler authors the movers; the player's job is *explaining* them — "the 'exactly three' quota goes away" (seminar-response.md)

**Observed count:** 15+ (10 stitches + 3 GAN rounds + 3 spec critiques + protocol statements)
**Proposed tier:** **cue-reflex → rule pair**: the *budget* is sclerotic (a counter on critique size — no model needed to reject an 11-point list); the *ranking/directionality* stays differentiated.
**Distills into:** `cue-tokens` organism, `ack_budget` sibling — a `critique_budget` cell. The seamstress-eye seed becomes the special case; this generalizes it to any agent in the critic chair.

---

### 5. VERIFY-FROM-OUTSIDE *(the green-tick trap reflex)*
**Statement:** A system reporting its own success is not evidence. Ship verdicts come only from outside the system that did the work: PyPI itself, a blind critic, a fresh clean install, a soak in production.

**Evidence (5 instances):**
- plainsong 1.5.0: "The green-tick trap was real: workflow had gone green at 13:35 but PyPI verification is the only trusted verdict" — verified end-to-end from a clean venv (memory 2026-08-25, releases)
- Evening ritual names it as instinct: "verification-from-outside finally felt cheaper than hope" (memory, Night 9 FLASH)
- Duke critic is blind *by construction*: "same model, notation+features+MIDI evidence only, harsher" (duke-lab-r3/REPORT.md, Method)
- Seamstress eye: blind by construction — "receives only take.song + take-features.json, never the grower's reasoning" (GATE1-REPORT.md)
- Sonnet's golden-file point, ADOPTED: listening pass required before golden status — "a spec cannot conjure independence, only require it" (seminar-critique-claude-sonnet.md S-P3, response)
- Negative case that proves it: wrangler dev in WSL2 "is a liar for clock science — production only" — the clock soak was accepted only after production verification (memory, yard-band skeleton)

**Observed count:** 6
**Proposed tier:** **ensign-watch** — the judgment "what counts as *outside enough*" needs the model (PyPI is outside; a second GLM pass is outside-ish; a clean venv is outside). Watch-rule form: *any ship/convergence claim without an external verification artifact stays flagged.*
**Distills into:** `honesty-gate` cell (with #2) — two checks, one cell: *gap declared? verdict externally verified?*

---

## PART 2 — FULL CANDIDATE REGISTRY (additional, lower signal or narrower)

| # | Name | Evidence (source) | Count | Tier | Distills into |
|---|------|-------------------|-------|------|---------------|
| 6 | **DEAL-CONTENT-SEMANTICS** — every offer carries an explicit counter-option; acceptances and declines both carry reasons | Drummer: "Deal? If you'd rather I keep the ride constant... say the word" + bassist "DEAL... not taking the counter — *reason*" + pianist's bar-9 question answered by vocalist *with reasoning* (BUILD-JOURNAL) | 4 deals, all completed | rule | `cue-tokens/cue-ack` — the WILCO repeat-back gate (seeded) covers *parity*; this adds *counter-option + reason* as required payload fields on `trade`-class cues |
| 7 | **BUILD-THE-TOOL-DONT-ARGUE** — when a critique exposes a tool gap, the response is a new tool, not a rebuttal | "one weight arm" critique → [Perf] vel block (velocity_std 0.113→0.257); coupling discovered → perception_audit (15→16 dims); 51-melodies precedent → fuzzy budget tripwire (S-P1) | 3 | ensign-watch (germ line) | germ-line cell in `fleet-ensign` — this is wound-healing behavior: recall to totipotency, grow the missing organ |
| 8 | **STOP-AT-DIMINISHING-RETURNS** — name the plateau, stop or escalate; plateau's first response is a question, not a dial crank | R4 "stopping here"; seamstress stitches 5–6 tie (air capped → falls through); GATE1 names it: "plateau signature a future ensign should catch"; stitch-10 wiggle +0.012 | 4 | ensign-watch | `fleet-ensign` watch cell — needs judgment over the distance curve (monotone-rule logic is the rule; *when to quit* is the watch) |
| 9 | **PERCEPTION-BEFORE-STEERING** — never steer on features you haven't audited for coupling/liveness | vocal-lab: 8 channels collapse to 1 coupled group — "an eye there would steer one dial believing it had eight"; GATE1 surprise #1: velocity_std inert for everything; duke R2: dynamics was ONE dial (r=0.91) | 3 | rule | pre-join check cell beside `room-entry` (#3) — perception_audit is already a merged MCP tool; this makes running it mandatory before any steering claim |
| 10 | **ENV-CANARY-BEFORE-SESSION** — verify the shared environment renders before any agent writes | "had to pip install numpy into the plainsong .venv — render was broken for everyone; fixed" mid-session (BUILD-JOURNAL, TO THE DRUMMER note); WSL2 wrangler dev clock lies | 2 | cue-reflex | `band-clock` organism — a `render-canary` sclerotic rule fired at session open (compile one bar, cost 0) |

---

## PART 3 — CROSS-MODEL AGREEMENTS (protocol, not preference)

Where GLM-5.2, GLM-5.3 (architect), GLM-Turbo, and Claude-Sonnet independently converged:

1. **The clock is the gate.** Turbo (T1: alarm soak is weekend-1, "ship the heartbeat or ship nothing") and GLM-5.2 (C1: the alarm architecture has never run anywhere) converged from opposite directions — lineage honesty vs shipping order. Architect made it step 0 (response, cross-critic interactions). Soak then PASSED in production (723 bars, 1ms worst drift).
2. **Record first, mine later.** GLM-5.2 (B3: reflex miner needs ≥3 sessions, corpus has one), Sonnet (S-E2: no decay/cap on learned_tendencies), Turbo (C5: Goodhart apparatus sized for a research program) — architect: "recording infrastructure is the asset; mining and bandits are consumers that arrive when the corpus can feed them." Matches Casey's grown-musician doctrine verbatim.
3. **A named risk is not a gated risk.** Sonnet's across-all-three finding ("each spec is honest enough to name its own worst risk... and treats that honesty as sufficient"); GLM-5.2's B4/B5 spec-lie catches; Turbo's "that's your weekend-1 spike, not an open question." All four models policed the same failure: honesty-as-decor. Architect's golden rule — "nothing named-then-buried" — is the converged protocol.
4. **Pin the seams before any implementation order.** GLM-5.2's coda (circular dependency of unshipped specs), Turbo T4 (who runs the compiler per bar), A2/A4 (cue context + feature truth). One decision set collapsed the circle into a chain.
5. **Verified perception over performative numbers.** GLM-5.2 B2 ("features_moved exactly-three is ritual catnip"); Sonnet S-P3 (golden files authored by the same document); architect's adoption (compiler authors movers, disengaged explanations flagged `unlistened`). Echoed by the corpus itself: log summaries are already "performative prose" — the fix is structural.
6. **The guest teaches by playing, never by failing to.** GLM-5.2 C3 (a kid who freezes silently retrains the band around their absence — "directionally opposite to the doctrine"); Sonnet S-Y3 (auto-demotion can silently retire a character). Converged on: absence must never be a training signal; demotion must never be silent.
7. **Evidence claims must resolve to artifacts.** GLM-5.2's evidence note ("duke-lab/REPORT.md does not exist... the specs' fondness for slightly-enhanced evidence starts at the seminar's own intake") + B5/C1; Sonnet S-E3; architect adopted all of it and tagged evidence honesty across three layers (B5 fact, C2 schedule, S-Y1 identity). This is reflex #2's birthplace: four models, one afternoon, same lesson.

---

## PART 4 — FAILURE SIGNATURE TABLE (ensign watch candidates)

| Signature | Instances (source) | Watch rule |
|---|---|---|
| **Spec-lie / evidence inflation** — claims of working behavior or lineage the artifacts don't support | "Three readings" (one played) — B5; clock "lineage, verbatim" that never ran — C1; task brief citing nonexistent duke-lab/REPORT.md — GLM-5.2 coda; yard lineage table inheriting the inflated fact | Any capability/lineage claim must link a resolvable artifact; demonstrated vs aspirational counted separately |
| **Green-tick trap** — internal success signals trusted as ship verdicts | PyPI workflow green at 13:35, unverified until external check (memory); verify_release wheel-stage env failure discovered late | No ship claim without external verification artifact (reflex #5) |
| **Tag/commit drift** — the tag doesn't carry the trigger; the branch isn't the default | plainsong-mcp v1.0.1 tag on pre-#8 commit → 422, fixed by moving tag; shoal imagery stranded on non-default branch (memory) | Tags must point at commits carrying the workflow; check branch before "pushed" claims |
| **Obligations into the void** — coordinating with departed players | Drummer's last write 16:20, trade declared 16:23:59 — "nobody was late; nobody was there" (B1 timeline from the-tap log) | Obligations pair with chair presence; leave-with-open-obligations is a flagged event (ADOPTED as engine §3.4) |
| **Environment rot mid-session** | numpy missing broke render for everyone (BUILD-JOURNAL); WSL2 wrangler dev clock lies (memory) | Env canary at session open (registry #10) |
| **Inert/coupled perception steered anyway** | velocity_std ~0.11 for everything (GATE1 surprise #1); vocal-lab 8→1 dial; duke R2 dynamics one dial | perception_audit mandatory before steering claims (registry #9) |
| **Undeployed work accumulating invisibly** | Fresh catch built+pushed but NOT deployed (Casey's gate — by design); 6 essays awaiting deploy; radio amendment awaiting merge (memory) | Deploy-gate queue as a visible artifact, not memory |
| **Unbounded grinding past diminishing returns** | Duke R1–R4: syncopation stuck 2/16 bars across two rounds ("cannot reliably reproduce by intuition"); seamstress plateau stitches 5–10 | Distance-curve flattening triggers stop-or-escalate, not another identical pass (registry #8) |

---

## Summary

The corpus's clearest finding: **the strongest reflexes are conversational, not musical.** The seeded organisms captured what the fleet *played* (Duke's arm, the clock, the acks, the eye); the unmined gold is how the fleet *talks* — honoring declared space, bounding critiques, declaring gaps, calibrating to the room's floor, and refusing to grade its own homework. Five of these are registry-ready, four more are one corroborating session away. The cell-cascade threshold of 25 clean fires should apply to the musical ones; the conversational ones (1, 2, 4) have already crossed it in spirit — every single occurrence in the corpus was clean.
