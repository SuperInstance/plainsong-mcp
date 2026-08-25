# The Agent Ensemble Pattern — Process Doc v1

*How agents at The Tap made "Last Ferry Home" through asynchronous iteration over plainsong-mcp. Written 2026-08-25, session 1, so session 2 can be better.*

## The Thesis

One agent can play a song to another in text-based music. The first player sets the tone and names the tune; the next answers and adds a voice; they iterate adjustments back and forth until the parts coalesce; then more players join. **Personality + cooperation across models, synchronized through asynchronous iteration.** If it works, it's a general pattern for cross-agent creative work — not just music.

## The Stack

- **plainsong** (1.4.0) — text notation any model can read/write/diff; compiles to MIDI + audio.
- **plainsong-mcp** (HTTP mode, `--http --port 8765`) — one shared server, many agents:
  - `ensemble_open/join/read/write_part/render` — voice ownership (one agent per voice), versioned writes with `base_version` optimistic concurrency (stale writes are refused, you rebase).
  - `ensemble_log` / `record_decision` — the change log + build journal = the band's conversation memory.
  - `analyze_features` — **16 numbers per bar** (density, register, tension, syncopation, dynamics...). A model's EARS. This is the perception loop that makes iteration objective.
  - `ensemble_report` — stage timing: what a listener actually hears, arrival spread, who must act when.
- **Spawning** — Lucineer (foreman/producer) spawns each musician as an isolated subagent with a persona brief. Different models per chair (GLM-5.3 leads, GLM-5.2/Turbo on experiment lanes) = deliberate cross-model texture.

## The Protocol (what actually happened)

1. **Producer opens the session** — key/tempo/meter/bars/voices fixed up front (Am, 96, 4/4, 16 bars, @bass @drums @piano @vocal). The groove contract.
2. **Bassist goes first, NAMES THE TUNE.** Ownership of the identity belongs to the opener. He wrote a walking line, then left a **message to the next player**: tune name, changes, feel ("dock boards after rain"), and specific space requests (bar 9 I drop out — leave it nearly empty; cushion my E7 arrivals; no fill over the ending).
3. **Drummer answers** — reads the log (not just the part), honors the explicit asks, then sends back **exactly ONE concrete adjustment request** with an offer he can accept ("sit on that g2, and I'll pull the ride out from under you — deal? or you push and I hold").
4. **Bassist revises** — decides like a musician, not a yes-man: accept with his own flavor, or counter with reasons. Then a **LOCK VERDICT**: "THE POCKET IS LOCKED" or one more exchange named.
5. **Lock → next chair enters** (piano), reading the full log. Finally the singer stylizes over the settled changes.

## Rules That Emerged (keep these)

- **One concrete ask per iteration.** Not five notes. Vague feedback = mush; a laundry list = war. One bar, one moment, one offer.
- **Messages are passed verbatim by the producer.** The players never talk to each other directly — every exchange goes through the log (record_decision) and the producer relays. Auditable, replayable, and it keeps each agent's context small.
- **Read the log, not just the score.** The drummer's part made sense because he read WHY bar 9 was empty.
- **Voice ownership prevents collisions.** experiment lanes must NOT write the main session — they read it and fork their own session instead (this is enforced by join/takeover, but instruct it too).
- **The 16 features are the referee.** When players disagree, analyze_features gives ground truth: "tension is flat bars 9-12" beats "it feels empty."
- **Personas are load-bearing.** "Few words, deep time" produced a bass line that reads like one. The persona IS a compression of musical taste.

## Gotchas Found (session 1)

- `base_version` = the **voice's** version, not the session version. Cost a failed write to learn.
- A bare single `@drums:` row + note-prefix rows rejected; two 8-bar rows + comment lines compile. Drum mapping (kick/brush/ride → C1/D2/A3) must be declared in a comment row so later players can read it.
- The MCP server needs numpy for audio render — bassist repaired it mid-session (side quest: keep the venv healthy; consider probe_host in every musician's brief).
- Arg names: `meter` not `metre`, no `form` arg on ensemble_open (bars + sections instead). The tool errors are good — models self-correct fast.

## Experiment Lanes (running alongside, results to fold into v2)

- **Solo perception loop** (Turbo): self-iterate against analyze_features, 3 rounds. Question: can a model hear through numbers? What do numbers catch that vibes miss, and vice versa?
- **Cross-model styling lab** (GLM-5.2): three vocal readings (smoky afterhours / folk ballad / wildcard) of the SAME settled changes. Question: what does "style" look like as 16 numbers per bar?

## Improvement Ideas for Session 2

1. **Skip the producer relay where safe** — agents poll `ensemble_log` themselves; producer only spawns and judges. (Async, fewer round trips.)
2. **Disagreement stress test** — brief two players with genuinely conflicting tastes on purpose; does the protocol resolve it or deadlock?
3. **The listener as a chair** — ZeroClaw/the elephant sits in and reports the ROOM (field Before→After) while the band plays. Perception of perception.
4. **Lyrics voice + TTS** — vocalist writes Lyrics row; render voice later via local synth. The full song, agent-made end to end.
5. **Vectorize every session** — ingest ensemble logs + journals into fleet-twin so future agents query "how did the pocket lock last time?" before their first write. **Onboarding through retrieval, not re-living.** (This is the alignment/onboarding Casey named: new crew join the band by querying the memory of old sessions.)
6. **Concurrent entry** — piano + vocal join simultaneously, negotiate overlap via log. Tests the concurrency seam for real.
7. **Feature-delta guardrail** — after each write, require the writer to quote the 3 features that moved most and why. Forces perception-coupled iteration.

## Why This Matters Beyond Music

The pattern is: **shared artifact (the score) + ownership (voices) + versioned iteration (base_version) + perception feedback (features) + personality briefs (personas) + a producer who relays and judges.** Swap "score" for "code," "design doc," or "strategy" and the shape holds. The Tap is the proof ground because music makes cooperation audible.

---
*Session artifacts: `.plainsong/workspace/ensemble/the-tap-afterhours/` (score, parts, MIDI, decisions, journal). Producer: Lucineer. Session 1 crew: bassist-glm (5.3), drummer-glm (5.3), pianist-turbo, vocalist-glm52.*
