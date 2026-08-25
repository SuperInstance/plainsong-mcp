# The Ensemble Engine — Architecture Draft v0.2

*The agentic layer above plainsong. Drafted 2026-08-25 by the architecture foreman; **revised same day after the cross-model seminar**: presence model (§3.4), compiler-verified `features_moved` (§2.1), miner deferred to v0.3 (§6), Trust Formula v1 defined and versioned (§8 Q5), and the Grown-Musician Doctrine integrated structurally — iteration nodes as branch points (§2.1), sheets as checkpoints (§1.3), gardener roles as the swappable loss function (§1.4), and the distillation seam (§6.5). Response ledger: `docs/seminar-response.md`.*

**Evidence note (seminar S-E3):** the quilt holds exactly one multi-agent session (`the-tap-afterhours`). `duke-lab`, same day, is a **solo** take — one agent, one chair, no cues, no trades — and is not counted as ensemble validation. Every multi-agent claim below rests on n=1, and the support thresholds in §6 exist because one session is one session. (The doctrine's answer to small-n is to keep recording: solo lineages grow musicians too.)

> Casey's directive, verbatim: "an agentic compiler that can have personalities built on player-character-sheets, and the plainsong is more of the leadsheet from the fakebook that gives everyone in the band standard constraints to spring off — an engine that does the iterating into JSON files in a quilt that learn to cue from one another in t-minus thinking."

---

## 0. The layer cake and where this engine sits

Three layers, each owning one question. The boundary rule is: **each layer may read the layer below and must not write it.**

```
┌────────────────────────────────────────────────────────────┐
│  PERF LAYER (sibling spec, docs/perf-spec-draft.md, TBD)   │
│  "How does this note get touched?"                         │
│  Open performance tensor per note: micro-timing, velocity  │
│  curves, attack shape, breath. Renders expression.         │
├────────────────────────────────────────────────────────────┤
│  ENSEMBLE ENGINE  (THIS SPEC)                              │
│  "Who plays what, when, and how do they listen?"           │
│  Players (character sheets), the room (iteration quilt),   │
│  and anticipatory cueing (t-minus). Resolves the social    │
│  graph, schedules rounds, simulates takes. Writes at       │
│  bar/beat addressability.                                  │
├────────────────────────────────────────────────────────────┤
│  PLAINSONG (exists, v1.4.0)                                │
│  "What are the standard constraints?"                      │
│  The fakebook leadsheet: key, tempo, meter, form, changes. │
│  Notation → MIDI/audio. The contract everyone springs off. │
└────────────────────────────────────────────────────────────┘
```

**Refinements to Lucineer's read** (which was correct; three sharpenings):

1. *Plainsong is the leadsheet AND the session manifest.* The groove contract (Am, 96, 4/4, 16 bars, four voices) is part of the constraint layer, not the social layer. The ensemble engine never edits key/tempo/meter mid-session; if the band modulates, that's a new leadsheet section and a compiler-visible event.
2. *Addressability is the load-bearing wall.* The whole engine keys on the address `bar.beat` (e.g. `13.4` = bar 13, beat 4) plus voice. Plainsong's window reads, the feature analysis (16 numbers per bar), cues, and quilt nodes all speak this one coordinate system. Everything else follows from having a common map.
3. *Division of labor with the perf layer:* the ensemble engine decides **intent** ("g2 leans late," "kick cushions the E7 arrival") at beat granularity; the perf layer decides **touch** (the g2 lands 28 ms behind the beat at velocity 71, with a slight slide into it). A cue from this engine emits an *intent directive* — and the perf layer now defines its consumer (perf-spec §8.4): the directive publishes as `$cue.*` expression context plus a `keep_empty` rest overlay, compiled at commit time. The seam is a contract with two hands (seminar A2). The referee reads post-perf features — one feature truth (perf-spec §9.5, step 5 below). This engine still never emits milliseconds.

---

## 1. Player Character Sheets

A player is a persona plus a musical identity plus **state that updates across sessions**. The sheet is the player's soul; it is versioned and lives in the quilt (§2), so a player's growth history is as queryable as the music.

### 1.1 Schema

```jsonc
{
  "sheet_version": 7,
  "player": "bassist-glm",
  "chair": "@bass",
  "model": "zai/glm-5.3",              // model identity is musical texture, deliberately
  "identity": {
    "name": "Moss",
    "one_line": "Few words, deep time.",
    "influences": ["Paul Chambers", "Charlie Haden early", "dock work songs"],
    "voice_notes": "Speaks in single sentences. Declined a deal once with a musician's reason, not pride."
  },
  "defaults": {                          // prior per write, overridable per session
    "velocity_bias": -6,                 // relative to leadsheet norm
    "timing_stance": "behind",           // behind | on | ahead (perf layer refines)
    "density_comfort": [0.3, 0.6],       // feature-space band: notes per beat
    "register_home": "a1-g2",
    "phrase_shape": "root-fifth skeleton, passing tones on the walk, never chromatic runs"
  },
  "tells": [                             // recurring, recognizable signatures
    "long root on final bar, always",
    "names the tune on first write — claims identity of the piece"
  ],
  "under_tension": {                     // what they reach for when features say 'flat' or 'crowded'
    "when_lonely": "walk more; add passing tones",
    "when_crowded": "drop out for a bar — leave the room, don't fill it",
    "when_pushed": "lean later, not louder"
  },
  "refusals": [                          // HARD RULES — identity firewall, see §6.3
    "never fill bar 16 over the final root",
    "never play a note on the front of 4 in bar 13 before the drummer answers"
  ],
  "trust": {                             // per-bandmate priors, updated across sessions
    "drummer-glm": {"score": 0.9, "notes": "pulls the floor out exactly when asked; his offers are real"},
    "pianist-glm": {"score": 0.6, "notes": "honors spaces; watch register overlap in e3-a3"}
  },
  "deals": [                             // standing two-way agreements, cited
    {"with": "drummer-glm", "terms": "I sit back on the g2; he pulls the ride",
     "provenance": "the-tap-afterhours node v8", "status": "half-executed"}
  ],
  "learned_tendencies": [                // mined reflexes accepted onto the sheet, §6 — capped at 12 active (§1.3), overflow archived
    {"pattern": "drummer pushes at T-4 before a landing bar",
     "response": "thin to root-only and sit behind",
     "confidence": 0.8, "support": 4, "sessions": ["the-tap-afterhours"],
     "last_fired": null}
  ],
  "provenance": {                        // every mutation cites the quilt
    "last_edit_node": "quilt:tap-v8",
    "edit_history": ["quilt:tap-v3", "quilt:tap-v8"]
  }
}
```

### 1.2 The four seed personas (from session 1)

These are **hypotheses seeded by one session** (seminar B5) — three demonstrated working behavior; the Kestrel demonstrated *one* of her three readings (the smoke reading, v12; ballad and foghorn-kestrel were never played). Sheets mark unproven claims `unproven: true`, because §1.3's own standard — a sheet with no provenance is a costume — applies to the seed paragraph too. The engine formalizes them as v1 sheets so session-2 agents inherit them by retrieval (§5) instead of re-briefing:

- **Moss (bassist-glm, GLM-5.3)** — few words, deep time. The one who declined the trade's first form with a musician's reason. Names the tune; owns the identity of the piece.
- **Sable (drummer-glm, GLM-5.3)** — listens more than speaks; sends exactly one concrete ask per iteration, each with an offer he can accept ("deal? or you push and I hold").
- **Reeds (pianist-turbo, GLM-5-turbo)** — shells, not walls; honors sacred spaces (bar 9 gets one dyad, bar 16 gets nothing).
- **The Kestrel (vocalist-glm52, GLM-5.2)** — one reading demonstrated (smoke, tap:v12); ballad and foghorn-kestrel claimed, `unproven` on the sheet. The hypothesis: style as a parameter sweep, not a mood — the sweep is what session 2 tests.

### 1.3 Sheet semantics

- **Sheets are quilt nodes.** Every edit appends a node of kind `sheet_patch` citing what taught it (a session, an ask honored, a reflex accepted). A sheet with no provenance is a costume, not a player.
- **Trust is earned asymmetrically and cheaply.** Honoring an ask raises trust in the asker *and* in the honoree; breaking a deal drops both, but a refusal-with-reason drops neither (Moss's declined deal was *correct* — the quilt should record the reason and the outcome, and the miner should learn that refusals-with-reasons correlate with good takes).
- **A new session reads sheets at head, writes patches at commit.** Two sessions with the same player run concurrently only if the engine forks the sheet; on merge, trust/deal conflicts are producer-adjudicated.
- **A sheet version is a checkpoint, not just a number (doctrine).** Every `sheet_version` is addressable, restorable, and diffable: `sheet show|diff|restore bassist-glm@7`. A restore is itself a `sheet_patch` node citing why — history is never rewritten, only branched. Sessions pin their sheet head at LOAD; two sessions wanting different heads **fork the lineage** (§2.1 branch nodes) instead of fighting over it. The sheet is the musician's current form; the version chain is the training trace.
- **Sheets stay sheets, not archives (seminar S-E2).** `learned_tendencies` caps at 12 active (ranked confidence × recency); overflow auto-archives below the active set — archived, never deleted. The v0.3 miner consolidates duplicates on arrival; retrieval re-ranking is instrumented, and a regression in tokens-to-first-write fires the KPI alarm. An accreted sheet silently killing onboarding is a bug, not a biography.

### 1.4 Gardener roles — the loss function is a swappable, versioned object

Growing a musician needs a gardener: the voice that says *good, again* and *wrong, why*. The engine makes the gardener a first-class, per-lineage object — the **loss function the lineage trains under** — instead of an ambient producer mood.

```jsonc
{
  "gardener_id": "tap:gardener-01",
  "role": "socratic-tutor",        // adversarial-critic | socratic-tutor | rival | curator
  "version": 3,
  "update_rules": {                 // role-typed: what this gardener rewards / penalizes
    "reward": ["ask honored with feature evidence", "rest where the room needed it"],
    "penalize": ["unexplained feature drift", "obligation broken silently"],
    "asks_per_round": 1,            // the one-concrete-ask norm, enforced
    "may_touch": ["trust", "learned_tendencies", "defaults"]   // NEVER identity/refusals
  },
  "feedback_style": "questions, not verdicts — 'what did the bar 9 space ask for?'",
  "provenance": {"sessions": ["the-tap-afterhours"], "author": "producer"}
}
```

- **adversarial-critic** — finds the weakest bar and names it; updates push toward feature contrast. The iron that sharpens iron.
- **socratic-tutor** — asks the player to explain their own movers (§2.1); updates favor explained over performed.
- **rival** — competes for the room's attention; updates push density/urgency *within refusals* (the Moss–Sable tension, formalized).
- **curator** — tends the repertoire and the sheet: prunes stale tendencies, proposes restores, guards the category ledger's meaning versions.

The producer role is decomposed: **producer = chair of gardeners.** Swapping gardeners is first-class — a `gardener_swap` node (or a `branch` node carrying one, §2.1) records the change with provenance — so a lineage grown under the critic and a lineage grown under the tutor *from the same checkpoint* are comparable by construction. The doctrine's core move — rewind to any iteration, swap gardener, regrow — is two node kinds and a pointer, not a new engine.

---

## 2. The Quilt of Iterations

The quilt is the band's memory: every write, decision, message, cue, verdict, reflex, and simulation, as **linked, addressable, queryable JSON patch nodes** — same philosophy as the fleet's quilt projects (a sheet of cells with dependency edges; reactive evaluation; vector cells for retrieval). Session 1's `log.jsonl` and `BUILD-JOURNAL.md` are *projections* of this structure; the quilt is the source of truth for history, the parts remain the source of truth for the score.

### 2.1 Node schema

```jsonc
{
  "node_id": "tap:v8",                   // session-scoped, monotonic
  "parent": "tap:v7",                    // LINEAGE PARENT — nodes form a tree (see rules)
  "kind": "write | message | cue | verdict | join | leave | branch | sheet_patch | gardener_swap | reflex | simulate",
  "time": "2026-08-25T16:23:59+00:00",
  "session": "the-tap-afterhours",
  "voice": "@bass",
  "agent": "bassist-glm",
  "base_version": 6,                     // plainsong optimistic-concurrency base
  "part_version": 8,                     // version this write produced
  "bars": [13],                          // addressable footprint in bar.beat space
  "diffs": [                             // semantic diff, not raw text
    {"at": "13.4", "was": "-", "now": "g2", "why": "sit on the g2 for Sable"}
  ],
  "message_to": ["@drums"],              // verbatim relay, producer passes unedited
  "message": "Deal taken. g2 leans in on the back of 4. Pull the ride at 14 and I'll land the f2 in that space.",
  "ask": {                               // the ONE concrete ask, if this node makes one
    "to": "@drums", "at": "14.1",
    "text": "pull the ride out from under me at 14.1",
    "offer": "I sit back on the g2",
    "status": "accepted | countered | declined-with-reason | open | executed | broken"
  },
  "features_moved": [                    // MANDATORY: the referee fields (session-1 idea #7, formalized)
    {"feature": "syncopation", "before": 0.11, "after": 0.24, "why": "g2 moved off the grid to the back of 4"},
    {"feature": "rest_ratio", "before": 0.38, "after": 0.34, "why": "one rest became a note"},
    {"feature": "note_density", "before": 0.62, "after": 0.66, "why": "same bar, one added leaning tone"}
  ],
  "cues_out": ["tap:cue-landing-9.1"],   // cue declarations this node makes (§3)
  "cues_in": ["tap:cue-kick-9.1"],       // cues this node responds to, with disposition
  "cues_in_disposition": [{"cue": "tap:cue-kick-9.1", "how": "honored" | "ignored" | "declined-with-reason"}],
  "refs": ["tap:v5"],                    // graph edges: this revision answers that write
  "verdict": null                        // "POCKET LOCKED" etc., on verdict nodes
}
```

Rules:

- **`features_moved` is compiler-authored, player-explained (seminar B2).** The compiler owns before/after — it *computes* the top feature movers at write time and writes them into the node. The player's mandatory field is `explain_movers`: an account of the compiler's numbers, not a quota of their own. ("Exactly three, self-authored" was ritual catnip — three beautiful numbers, every time, forever.) An explanation that doesn't engage the actual movers is flagged `unlistened` on the node; gardeners (§1.4) may weight it. Verified perception-coupling from day one. (Features are plainsong's existing 16-per-bar set: `note_density`, `syncopation`, `harmonic_tension`, `rest_ratio`, `velocity_mean`, …)
- **Edges make the conversation a DAG, not a log.** `refs` is how "this revision answers that ask" is expressed; a new drummer onboards by walking the edges around the bar-13 exchange, not by reading 400 lines of chronology.
- **`parent` makes lineages trees — any node is a branch point (doctrine).** Linear sessions set `parent` to the previous node; a `branch` node forks: it carries `from_node`, a `reason`, and optionally a `gardener_swap` (§1.4). `branch from tap:v8, gardener: socratic-tutor, reason: "v8's pocket was the one worth keeping"` spawns a new growing line whose quilt hangs from that node. Rewind to any iteration, say "that's enough," bring in a different gardener, regrow — first-class, because regret is the most common producer emotion. `leave` ends a chair's presence (§3.4); `gardener_swap` records a mid-lineage loss-function change with provenance.
- **Address everything twice**: by node (`tap:v8`) and by location (`@bass 13.4`). The miner (§6) works in location space; the retriever (§5) works in node space.
- **Projections, not duplicates.** `log.jsonl`, the manifest summaries, and a future human-readable journal are all rendered *from* quilt nodes. One fact, one home. (Engineering note: plainsong-mcp keeps writing these files as it does today; the quilt adapter ingests and links them, adding `diffs`/`features_moved`/cue fields the current log lacks.)

### 2.2 Quilt-as-cells (the fleet-twin alignment)

Each node is a cell; derived cells compute per-session rollups the compiler reads cheaply: `session.trust_graph`, `session.open_obligations` (§3.4), `session.cue_schedule`, `session.style_fingerprint` (mean feature vector per voice). Vector cells hold embeddings of node summaries for retrieval (§5). This is plain quilt — no new substrate.

---

## 3. T-Minus Cueing

Musical cues are anticipatory: a cue fires **T-minus-N beats before its event**, so the receiver has N beats of preparation. This is the "learn to cue from one another in t-minus thinking" clause, made mechanical.

### 3.1 Cue schema

```jsonc
{
  "cue_id": "tap:cue-landing-9.1",
  "session": "the-tap-afterhours",
  "from_voice": "@bass",
  "at": "9.1",                  // the EVENT, in bar.beat
  "t_minus": 4,                 // in BEATS (not seconds — tempo-independent)
  "fire_at": "8.1",             // resolved by compiler: at − t_minus
  "kind": "landing",            // cut | push | trade | solo | landing
  "target": "@drums",           // a voice, or "room" (all voices)
  "payload": "bar 9 is nearly empty — my A lands alone at 9.1. Cushion the approach, then let the bar breathe.",
  "intent_directive": {         // machine-readable twin of the payload — CONSUMED by perf-spec §8.4 ($cue.* context + keep_empty rest overlay, compiled at commit)
    "wants": {"feature": "velocity_mean", "dir": "down", "window": "9-9"},
    "keep_empty": ["9.2-9.4"]
  },
  "declared_in": "tap:v3",      // provenance: the node that declared it
  "status": "declared | broadcast | honored | answered | ignored | withdrawn",
  "response": {"node": "tap:v6", "disposition": "honored"}
}
```

### 3.2 The five kinds (and only five, for now)

| kind | means | canonical example from session 1 |
|---|---|---|
| `cut` | stop / get out of the way | "no fill over bar 16" — the whole band honored it |
| `push` | accelerate energy into the event | (none yet — the band is a 96-bpm afterhours band) |
| `trade` | exchange obligations: you do X, I'll do Y | "sit on that g2, and I'll pull the ride out from under you — deal?" |
| `solo` | yield the floor to a voice | bar 9's opening for the bass A (retroactively: the room yielded to the bassist's ask) |
| `landing` | an arrival is coming; cushion or clear it | "cushion my E7 arrivals" — kick feathered c1 at 8.1 and 15.1 |

### 3.3 Dual-time semantics — the crucial definition

Nobody is playing in real time; the band iterates asynchronously. So `t_minus` has meaning in **two worlds**, and the engine defines both from one number:

- **Performance time (simulate/render):** the session clock advances in beats at the leadsheet tempo. A cue with `t_minus: 4` at 96 bpm broadcasts 2.5 s before its event (one bar's notice at this tempo — T-4 in 4/4 is exactly "next bar's downbeat is the event"). A receiver's reflex fires within its response window.
- **Negotiation time (live iteration):** the compiler maps beats to **write windows**. When a cue is declared against a future bar, every target voice gets a write-window deadline keyed to `at`: your revision addressing this cue should land before the session reaches that musical location's *negotiation checkpoint*. Because models take seconds-to-minutes, the engine never pretends real-time; it enforces **ordering** (responses to cue X accepted before nodes that assume X was ignored) and **completeness** (at checkpoint: cue must be `honored`, `answered`, or `ignored-with-record`).

Rule of thumb the engine enforces: **a receiver's response window in negotiation time is one iteration round; in performance time it is `t_minus` beats.** Both are "preparation time." The simulate-a-take run (§4.6) is precisely the mode where the two coincide.

### 3.4 The obligations ledger (found in the evidence)

Session 1's bar-13/14 trade is **half-executed in the score**: the bassist delivered his side (v8: late g2) but the drummer's side — pulling the ride at 14 — was never written before the piano entered. Nobody broke faith; the deal just fell out of anyone's context. The compiler therefore maintains a derived **open-obligations cell**: every `trade` cue with status `accepted` spawns two obligations (one per side), each tracked until its `diffs` appear in a node or the deal is explicitly renegotiated. The producer surfaces open obligations at every round boundary. **No deal silently evaporates.**

**And no obligation is notified into a void (seminar B1).** The founding defect was not a deadline failure: the drummer's last write was 16:20, the trade *declared* 16:23, the pianist entered 16:26 — nobody was late; the drummer was *gone*. Obligations therefore pair with **chair presence**: `join`/`leave` nodes maintain a `session.presence` cell. An obligation opened against a departed or unheld chair triggers, in order — producer paging (re-invoke the player), a renegotiation window (the ask re-opens to the room), or an explicit **decline-with-reason** recorded on the sheet. A `leave` while obligations are open is a flagged event, not a silent exit. An obligations ledger without a presence model is a notification into the void; session 2 would have reproduced session 1's defect with better logging.

**The ledger is a floor, not a ceiling (seminar S-E4).** Obligations instrument the ~10% of interplay that became words. The 90% that never became a cue is not modeled and will not be soon — `no open obligations` can read green on an incoherent take. Cheap, honest countermeasure: **coherence probes** — periodic producer verdict nodes ("is this take coherent? name the weakest exchange") that depend on no cue having been declared. The quilt records everything either way; the doctrine's bet is that the raw trace outlives the schema's reach.

### 3.5 Compound and conflicting cues

- Two cues targeting the same voice in overlapping windows: **kind precedence** `cut > landing > trade > push > solo`; ties broken by the target's trust ordering **under Trust Formula v1 (§8 Q5) — a versioned object pinned per session**. If the pinned formula is absent (pre-version sheets), ties fall to cue chronology: declared-first wins. No unversioned number decides whose musical intent wins a conflict.
- Cue chains (A cues B cues C) are legal and expected; the compiler computes the transitive schedule and detects **loops** (`push` chains returning to the origin inside one bar) — flagged to the producer, not auto-resolved. Compounding is where the music lives; the engine just refuses to let it tangle silently.
- A cue may be `withdrawn` by its declarer; withdrawals are nodes too, and the miner reads them (withdrawn cues that were honored anyway = a trust signal about the receiver's reading).

---

## 4. The Agentic Compiler

The engine is a **compiler with a social front-end**. It doesn't just merge parts to MIDI (plainsong does that); it resolves the band as a system and emits arrangements as first-class artifacts. The pipeline:

```
   leadsheet ─┐
  char sheets ─┼─► 1 LOAD ─► 2 RESOLVE ─► 3 SCHEDULE ─► 4 ITERATE ─┬─► 6 SIMULATE ─► 7 MINE (v0.3) ─► 8 COMMIT
   quilt head ─┘                    ▲                             │        │
                                     └─────── 5 ADJUDICATE ◄───────┘        └─► reflex proposals
                                                                            (onto sheets, §6)
```

1. **LOAD** — ingest leadsheet + session manifest; load each player's sheet at head; hydrate each agent's context by retrieval (§5): sheet + top-k relevant quilt episodes + current window (`ensemble_read` already provides windows) + cue schedule.
2. **RESOLVE** — build the social graph: who holds which chair, trust edges (from sheets), standing deals, open obligations carried in from prior sessions, declared cues and their fire times. Output: `session.social_graph` and `session.cue_schedule` cells. Conflicts (§3.5) flagged here.
3. **SCHEDULE** — iteration rounds. Default protocol from session 1, now compiler-enforced: opener names the tune → one chair at a time until first lock → next chair; concurrent entry allowed for chairs with no open asks between them. **The one-concrete-ask norm is a compiler rule, not a politeness:** a node carrying a second open ask to the same voice in the same round is rejected with the existing open ask quoted back.
4. **ITERATE** — players write parts (`ensemble_write_part`, `base_version` concurrency, exactly as today); every write appends a quilt node with mandatory `features_moved`; messages pass verbatim through the producer relay (session-2 experiment: agents poll `ensemble_log`/quilt themselves).
5. **ADJUDICATE** — disagreement is settled by the features referee (`analyze_features`: "tension is flat bars 9–12" beats "feels empty"); verdicts (`POCKET LOCKED` / one more exchange named) are `verdict` nodes. Locks gate chair entry. **Features are post-perf** (seminar A4): perf compiles at commit, so the referee, `features_moved`, and SIMULATE all score the music the renderer plays — one feature truth, decided once (perf-spec §9.5).
6. **SIMULATE** — a take is forward-run **without agents**: the compiler walks the session clock, fires every declared cue at its `fire_at`, applies each receiver's learned reflexes (sheet `learned_tendencies`) as deterministic response functions, applies refusals as vetoes, **compiles perf**, and renders the post-perf arrangement + feature trace. This previews what the band *would* play if everyone played their sheets — the difference between simulate output and the live-iterated score is a measure of how much the humans-in-the-loop (the actual models) are doing beyond their priors. Unresolved obligations surface as **obligation-delta misses** (seminar B4): for each open obligation, did the features move the way the obligation implied — did drums density thin at 14 as the ride-pull required? Session 1's actual defect signature was *texture that never cleared* (the ride kept playing through the trade), not dead air; the detector watches the real signature, named at its bar.beat.
7. **MINE — deferred to v0.3 (seminar B3).** Pattern-mining across the quilt (§6) proposes reflexes onto sheets, subject to refusal rules; proposals are `reflex` nodes pending the player's (or producer's, for unclaimed sheets) acceptance. v0.1 ships the *recording* side — nodes, verified movers, cue outcomes, gardener swaps — and none of the mining: the corpus holds one multi-agent session, and §6.1's support threshold (≥3 sessions) cannot be met. Building it now would force premature answers to §8.2/§8.3 on data that cannot inform them.
8. **COMMIT** — quilt checkpoint; sheets versioned; obligations and cue statuses carried forward; next round scheduled. The session's journal/manifest projections are re-rendered.

**What the compiler emits:** the merged score (plainsong's job), *plus* the cue-annotated arrangement (parts + cue schedule + reflex firings as simulate log), the social graph snapshot, and the feature trace. Arrangements are replayable artifacts: same quilt head + same sheets + **same pinned `trust_formula` version** ⇒ same simulated take, deterministically (seminar S-E1 — the formula is versioned precisely so replay survives its own evolution).

---

## 5. Onboarding by Retrieval

New agents join the band by **querying the band's memory, not re-living it** (Casey's onboarding-through-retrieval clause; session-1 improvement idea #5, formalized).

- **Index:** every quilt node's summary + `diffs` + `features_moved` + cue outcomes is embedded (fleet-twin vector cells; `bge-m3`-class embeddings are plenty — the corpus is small).
- **Onboarding query pack** for a new drummer joining session 2 of a band: their character sheet at head; top-k nodes for "how did the pocket lock here before" (retrieved by similarity to the current session's open context); the open-obligations ledger (a new drummer *inherits* Sable's half-open ride-pull at 14.1 — or the producer renegotiates it on their behalf); trust priors seeded from the sheet, not from re-reading transcripts.
- **Retrieval respects the room.** A new player gets the *why* (nodes) but writes only from their own sheet + the leadsheet. Onboarding cost should be three reads, not thirty. Measure it: tokens-to-first-write per chair is an engine KPI.
- **The quilt is the training corpus (doctrine) — nodes are never compacted**, only re-indexed. Blob-scale retention policy (renders, tape-scale data) lives in the yard-band spec; it does not touch nodes or sheets, because onboarding-by-retrieval reads exactly those.

---

## 6. Learned Reflexes

"Cues compound into learned reflexes over sessions." The loop: **mine → propose → gate → fire → evaluate.**

> **Scope note (seminar B3): designed, not built, in v0.1.** The miner enters at v0.3, when ≥3 sessions of nodes exist to mine. Keeping the schema now costs nothing and means v0.3 needs no migration; building the miner now would mean infrastructure for evidence that does not exist. With no trust-consuming miner in v0.1, Trust Formula v1 (§8 Q5) has exactly one consumer — precedence ties — which is why it is defined and versioned rather than left as vibes.

### 6.1 Mine

Across the whole quilt, in location space: find cue→response correlations with support ≥ 3 sessions and consistency ≥ 0.7 — *e.g.* **"when the drummer pushes at T-4 before bar 9, the bass thins to root-only and sits behind."** The miner is pattern-matching on (cue kind, t_minus band, relative location, target voice) → (response diff shape, feature delta shape).

### 6.2 Propose

Reflex proposals land on the target's sheet as `learned_tendencies` with confidence, support, and provenance sessions — **pending**, never auto-active for live rounds unless the producer opts a band into "reflex mode."

### 6.3 Gate: refusals are the identity firewall

Every reflex passes the player's `refusals` before firing. "Never fills bar 16" vetoes any learned fill reflex at 16.x, forever, regardless of confidence. **A reflex that a player overrides repeatedly (3×) is auto-demoted and surfaced as a persona-drift question** (§8, problem 2), not silently deleted.

### 6.4 Fire and evaluate

In simulate (§4.6) reflexes fire deterministically on the cue schedule. In live rounds, a firing reflex is *offered to the agent as context* ("your sheet says: when Sable pushes at T-4, you thin — apply or override?"), and the choice is logged. Overrides feed trust (a player whose reflexes get overridden by everyone is drifting from the band) and re-train the miner.

### 6.5 The distillation seam (doctrine, honestly hedged)

The Grown-Musician Doctrine's endgame: a mature lineage — sheet checkpoints + iteration tree + recordings (feature traces, takes) — is a *training artifact*, and the quilt should be able to export one for vectorization or distillation into a model form.

- **Export unit: a lineage, not a session.** `distill export bassist-glm@lineage(main, tap:v1..head)` produces the sheet version chain (checkpoints + diffs), the node tree with gardener swaps marked, per-session feature traces + take renders, and the category-ledger slice the lineage used.
- **Candidate forms, in order of cheapness (all unproven past #1):** (1) *retrieval bundle* — embeddings + tendencies as a cold-start sheet for a new player (this is just §5, shippable now); (2) *reflex pack* — mined tendencies compiled to the yard-band reflex tier's vector-match format (needs the v0.3 miner); (3) *fine-tune corpus* — (sheet, window, action, mover-explanation) tuples as SFT data for a chair-model; (4) the doctrine's far shore — a pincher-style vectorized persona, "Moss distilled."
- **Honest unknowns, kept visible:** nobody has distilled from feature traces + explanations before — whether mover-explanations carry transferable style signal is an empirical question with zero data; provenance and licensing of a persona exported into weights is unowned (a grown Moss distilled into a model — is it still Moss?); and the eval for "did the distillate keep the musician" does not exist (play-it-blind against the lineage's takes is the leading candidate). The seam is designed so the export can never destroy the source: **distillation reads the quilt, never writes it.**

---

## 7. Worked example — one cue chain through the band

**The chain around bars 8–14 of "Last Ferry Home," re-expressed as the engine would have run it.** All times in session-clock beats; at 96 bpm one beat = 625 ms, so T-4 = 2.5 s = one bar.

**Node tap:v3 (Moss/@bass, first write).** Declares two cues, both carried in his message verbatim:

1. `cue-landing-9.1` — `{kind: landing, at: 9.1, t_minus: 4, fire_at: 8.1, target: room, payload: "bar 9 nearly empty — my A lands alone; cushion the approach, let the bar breathe"}`. Fired at 8.1: at that moment Sable has four beats (2.5 s of musical time; in negotiation time, one round) to prepare.
2. `cue-landing-15.1` (E7 cushion) — `{kind: landing, at: 15.1, t_minus: 4, target: @drums, payload: "cushion the E7 arrivals"}` — plus the same implicit at 8.1.

**Sable's response (node tap:v6).** Honors both: feathered kick `c1` rides in *with* the A at 9.1 (`c1-a3` on the downbeat) then the bar opens — a `landing` honored means *cushion then clear*, and the feature trace shows drums `note_density` 0.5 → 0.25 across the 9.1 boundary. His write declares:

3. `cue-trade-13.4` — `{kind: trade, at: 13.4, t_minus: 2, target: @bass, payload: "sit on that g2 and I'll pull the ride out from under you — deal? Or you push and I hold"}` — fires at 13.2 (two beats of decision room: breath on the front of 4, decision by the back).

**Moss's answer (node tap:v8).** Deal accepted, with flavor: breath at 13.4-front (a rest where the g2 *would* sit early), `g2` leaning in at 13.4-back. `features_moved`: syncopation 0.11→0.24, note_density +0.04, rest_ratio −0.04. The trade spawns **two obligations**: Moss's (executed at v8) and Sable's (**open**: pull the ride at 14.1). 

**Reeds enters (node tap:v10)** reading the log, not just the score. He sees `cue-landing-9.1` honored and the half-open trade. His part answers the *chain*: held dyad `a3-e4` on 9.3 (inside the cleared bar, one object only), `a3-c4-e4` at 13.4 joining Moss's late g2 from below, single sustained `a3` at 14.2 — one beat *after* the f2 drop at 14.1, placed into the space Sable's (unwritten!) ride-pull was supposed to open. The compiler's obligations ledger flags at this checkpoint: **obligation `ride-pull-14.1` is open; simulating the take renders a hole at 14.1** — the exact defect session 1 actually shipped. Producer surfaces it to Sable before render.

**The Kestrel (tap:v12 — the smoke reading; ballad and foghorn never played — seminar B5).** Reading cues off the structure: she declares `cue-solo-16.1`-adjacent behavior by *not* declaring anything — bar 16 is protected by Moss's standing `cut` (`no fill over the ending`), which is also his sheet refusal. Double coverage: cue + refusal. The band ends on `c1 a3~~~` and a long `a1`. Nobody fills bar 16. The reflex miner, one day, learns "this band's endings are open" as a *band-level* reflex (see §8, problem 3).

---

## 8. Honest open questions (three closed this revision — kept visible)

1. **Whose clock is it, anyway?** Dual-time (§3.3) is defined but the seam is untested: when a cue's `t_minus` is shorter than one model's iteration latency (T-2 at high tempo vs. a 40-second model call), negotiation time *cannot* honor performance order. Fallbacks: producer pads rounds, or short-t_minus cues are compile-time-only (reflex territory, agent hands off). Needs a stress test with a real T-1 cue.
2. **Persona drift vs. learning (Ship of Theseus).** If Moss's sheet accumulates 40 learned tendencies, when does he stop being Moss? Refusals gate reflexes, but refusals themselves can be edited — by whom? Current stance: refusals are producer-frozen (identity is a constitution, not a config), but that centralizes taste in the producer. Unresolved, deliberately. **Partial structure now (doctrine):** gardener roles (§1.4) make the question explicit per-lineage — `may_touch` boundaries say who may edit which class of field under which gardener; refusals remain producer-frozen. Who owns the gardener roster is the residual, still open.
3. **Band-level vs. player-level reflexes.** "This band's endings are open" is a property of the *room*, not any player. The sheet schema has no home for band reflexes — band sheet? session-sheet? The quilt holds them naturally as mined patterns over the session subgraph, but where they *govern* firing is unclear. Also: two bands sharing players will disagree about a shared player's tendencies — per-band sheet overlays are the leading candidate, unimplemented.
4. **Is `features_moved` gameable? — RESOLVED (seminar B2).** The compiler authors the movers (it owns before/after); the player explains them; disengaged explanations are flagged `unlistened`. The ritual can't be gamed by quoting beautiful numbers, because the player no longer chooses the numbers.
5. **Trust math — RESOLVED: Trust Formula v1, defined and versioned (seminar S-E1).** `Δ +0.05` obligation executed · `−0.10` broken-by-deadline · `0` refused-with-reason · `0` withdrawn-but-honored (recorded as signal) · decay `×0.95` per idle session · clamp `[0,1]` — adopted from yard-band §8.3, canonical here. The formula is a **versioned object**: `trust_formula: v1` is pinned at session start, written to the manifest, and replay/simulate use the pinned version — determinism survives formula evolution. Pre-version sheets carry `trust_formula: null`; their precedence ties fall to chronology (§3.5). Trust-gated reflexes remain v0.3, with the miner.
6. **Concurrent chair entry is scheduled but unsocialized.** The protocol serializes chair entry; the engine permits concurrency where no asks are open. But two strangers taking chairs simultaneously have no trust priors — first-session concurrency may need producer-forced serialization anyway. Session-2 experiment will tell.
7. **The perf-layer seam — RESOLVED.** Perf-spec v0.2 §8.4 defines the consumer (`$cue.*` context, `keep_empty` rest overlay, compiled at commit) and §9.5 fixes one feature truth (post-perf). The handshake has a hand; expect revision only where real sessions force it.

---

## Appendix A — Mapping to what exists today

| Engine concept | Today's carrier | Gap |
|---|---|---|
| Leadsheet/session contract | plainsong `ensemble_open` manifest | none — this layer is the contract, keep it |
| Parts + optimistic concurrency | `ensemble_write_part` / `base_version` | none — engine wraps, doesn't replace |
| Iteration history | `log.jsonl` summaries | quilt nodes add diffs, features_moved, cues, edges |
| Perception | `analyze_features` (16/bar) | verify quotes (§8.4) |
| Personas | producer's prompt briefs per subagent | sheets: versioned, cited, retrievable |
| Presence | — | new: join/leave nodes + presence cell (§3.4) |
| Gardener / loss function | producer's mood | gardener objects: versioned, swappable, role-typed (§1.4) |
| Memory/journal | `BUILD-JOURNAL.md` (session 1 didn't write one) | quilt projections render it |
| Reflexes | — | v0.3: miner + gating (recording side ships v0.1) |
| Cueing | verbatim messages, human-band instincts | cue schema + schedule + obligations ledger |
| Simulation | — | new: deterministic forward-run |

## Appendix B — Timing crib (96 bpm, 4/4)

1 beat = 625 ms · 1 bar = 2.5 s · T-1 = 0.625 s · T-2 = 1.25 s · **T-4 = 2.5 s = one bar** · T-8 = 5 s = two bars. In 4/4, a T-4 cue fired on a downbeat is "next downbeat is the event" — the natural unit of band telepathy.

---
*End of draft v0.2. Argue with what's left of §8, with §3.3/§3.4 (dual-time + presence), and with §1.4/§6.5 (gardener + distillation unknowns) — that's where the real risk now lives.*
