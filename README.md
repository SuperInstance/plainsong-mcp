# tapscript-mcp

A Model Context Protocol server for [TapScript](https://github.com/SuperInstance/tapscript-studio),
so any agent can read, write and compile music notation — and so several agents
can work on one score at the same time without overwriting each other.

```bash
tapscript-mcp                 # JSON-RPC over stdio, what most clients expect
tapscript-mcp --http          # loopback HTTP, for remote and multi-agent setups
tapscript-mcp --list-tools    # what it exposes
```

## Install

```bash
pip install git+https://github.com/SuperInstance/tapscript-mcp
```

That brings in the compiler as well. Neither has any other dependency: the
protocol, both transports, the session store and the compiler itself are
written against the standard library. Python 3.10 or newer.

The compiler is currently pulled from a branch of
[tapscript-studio](https://github.com/SuperInstance/tapscript-studio) rather
than from its default branch, because the package this builds on is still in
review there. Installing works; the pin moves the day that merges.

## Point a client at it

For a client that launches servers over stdio, the usual shape is:

```json
{
  "mcpServers": {
    "tapscript": {
      "command": "tapscript-mcp"
    }
  }
}
```

Then ask it for music. The server exposes 27 tools, which is everything the
`tapscript` CLI can do — write and validate notation, compile to MIDI and
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

## Where this came from

This began inside the compiler's repository and was extracted once it was clear
it had become its own thing rather than a feature of the compiler. Two names had
also collided along the way: the analysis of who hears what on a physical stage,
and a session shared by several agents, were both called "ensemble". The first
is now `tapscript stage` and lives with the compiler; the second is what this
repository means by the word.

The compiler still ships a copy of this server, which is what its `tapscript
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
