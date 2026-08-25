# plainsong-mcp

<p align="center">
  <img src="assets/images/hero.jpg" alt="Agents composing — the MCP seam between notation and sound" width="640">
</p>

A Model Context Protocol server for [Plainsong](https://github.com/SuperInstance/plainsong),
so any agent can read, write and compile music notation — and so several agents
can work on one score at the same time without overwriting each other.

```bash
plainsong-mcp                 # JSON-RPC over stdio, what most clients expect
plainsong-mcp --http          # loopback HTTP, for remote and multi-agent setups
plainsong-mcp --list-tools    # what it exposes
```

## Install

```bash
pip install git+https://github.com/SuperInstance/plainsong-mcp
```

That brings in the compiler as well. Neither has any other dependency: the
protocol, both transports, the session store and the compiler itself are
written against the standard library. Python 3.10 or newer.

The compiler comes from PyPI as `plainsong>=1.4.0`. 1.1.0 is the first release
carrying `plainsong.features`, the per-bar analysis this package re-exports
rather than duplicating; 1.4.0 is the first carrying `plainsong.runtime.localhost`,
the loopback check behind the same re-export, so 1.4.0 is now the binding floor.
Either way the requirement is real: below it the install succeeds and the
import fails.

## Point a client at it

For a client that launches servers over stdio, the usual shape is:

```json
{
  "mcpServers": {
    "plainsong": {
      "command": "plainsong-mcp"
    }
  }
}
```

Then ask it for music. The server exposes 27 tools, which is everything the
`plainsong` CLI can do — write and validate notation, compile to MIDI and
audio, transpose, search a library of several thousand pieces, analyse what
each listener on a stage actually hears, and probe what the host machine can
render.

## Many agents, one score

The reason this exists. A session gives every agent a voice of its own:

```
ensemble_open    name a session, set key, tempo and metre
ensemble_join    claim a voice -- one owner at a time
ensemble_read    the whole current state, in one call
ensemble_write_part   write your voice, against the version you read
ensemble_render  merge the parts and compile
ensemble_log     what everyone has done
```

Because the parts are disjoint, the common case never conflicts — two agents
writing two voices both succeed. When two do collide, the later write is
refused and handed the current state to rebase onto, rather than silently
overwriting somebody's work. Locks are held only around a read-modify-write of
the manifest, never across a call to a model, because a model call takes
seconds and a lock held that long is a lock nobody else can get.

Notation is parsed before a part is accepted, so invalid notation never lands.
Writes are atomic, the merge is deterministic, and every change appends to a
log a joining agent can read to find out what has happened so far.

See [docs/ensemble.md](docs/ensemble.md) for the whole protocol and
[docs/mcp.md](docs/mcp.md) for the tool and resource surface.

## Reading a score as features

`analyze_features` computes sixteen per-bar features — note density, harmonic
tension, syncopation, contour direction, register spread and so on — matching
the vocabulary [fleet-jepa-midi](https://github.com/SuperInstance/fleet-jepa-midi)
perceives. That lets a bandleader read a written score, and makes a corpus of
notation usable as labelled training data.

Three more instruments serve the perception loop directly, each closing a seam
the pulse-eye retrospective found (tensor-midi, 2026-08-25): everything the
loop needed was in the per-bar stream, and the summaries averaged it away.

- `perception_trace` — the per-bar rows of a session, all sixteen channels,
  and deliberately no mean. A pocket lock was one bar among sixteen; a
  consumer that reads averages will never see it. `analyze_features` returns
  these rows too — the seam was never that the data was hidden, but that
  consumers collapsed it early.
- `perception_audit` — variance and correlation over the sixteen channels,
  and a verdict per channel: DEAD (zero variance in the texture and every
  voice — a dial connected to nothing), COUPLED (|r| > 0.9 with another
  channel — one steering dimension, not two) or ALIVE. Orthogonality of
  steering channels is the difference between growing and stalling; the
  audit counts the degrees of freedom a loop actually has. Run against the
  seamstress gate-1 session it reads: 16 channels → 6 steering dimensions
  (7 dead, 4 coupled into 1) — register was the only live growth channel,
  which is what the growth curves had already shown.
- `dimension_stats` — one named annotation row of a session (`Breath:`,
  `Gaze:`, anything a composer can write) as count, mean, std and a per-bar
  series, so an eye can see custom dimensions, not just velocity. This sits
  on a compiler capability that is **not in a plainsong release yet**: generic
  annotation rows live on the unmerged `dynamics-and-swing` branch of
  SuperInstance/plainsong (built on `annotation-rows`). On a compiler without
  it the tool answers with an error naming the missing capability, and a
  `Breath:` row in a part is kept as free text. Nothing is vendored; when the
  branch merges, the tool starts reading with no change here.

## Where this came from

This began inside the compiler's repository and was extracted once it was clear
it had become its own thing rather than a feature of the compiler. Two names had
also collided along the way: the analysis of who hears what on a physical stage,
and a session shared by several agents, were both called "ensemble". The first
is now `plainsong stage` and lives with the compiler; the second is what this
repository means by the word.

The compiler still ships a copy of this server, which is what its `plainsong
mcp` command runs. That copy is being retired — install from here.

## Status

The protocol is exercised by a test suite that drives the server with real
JSON-RPC: the `initialize` handshake, `tools/list`, `tools/call`, malformed
input, unknown methods, notifications, and a tool that raises. Concurrency is
tested with threads racing for the same voice, and merge determinism is checked
by writing the same parts in three different orders and comparing bytes rather
than assuming.

CI runs the suite on Python 3.10 through 3.13 across Linux, macOS and Windows,
and then speaks the protocol to the built server over a pipe, so a handshake
that regresses fails the build rather than a mock of one.

No third-party MCP client has connected to it yet. The protocol behaviour is
verified against the specification rather than against a particular client —
strong evidence, and not the same thing. Doing that is the most useful thing
anyone could contribute.

90 tests.

## Licence

MIT. See [LICENSE](LICENSE).
