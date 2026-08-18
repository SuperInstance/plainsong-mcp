# Changelog

## Unreleased

### The HTTP transport was open to DNS rebinding

`_same_origin` compared `Origin` against `Host` and nothing else. That is
defeated by rebinding: point `evil.example` at 127.0.0.1 and a browser sends
`Host: evil.example` with `Origin: http://evil.example`. They match perfectly,
the same-origin check passes, and a page on the open internet is talking to a
local tool that can read and write files.

What a rebound request cannot do is claim a **loopback Host**, so that is now
required as well. Two tests cover it — a rebound host is refused, and the
ordinary loopback hosts still work, because a guard that locks out the case it
is protecting is not a fix. Removing the check turns the suite red.

The guard already existed in `plainsong/mcp/server.py`, the copy inside the
compiler, and had never reached this one. That is the duplication this
repository's `CLAUDE.md` warns about, producing exactly the outcome it predicts:
a security fix in one copy and not the other, for months, with nothing able to
notice. **This copy is the one people install for MCP.**

### The package docstring pointed at the other package

It told the reader to run `python -m plainsong.mcp` — the compiler's copy —
from inside this package's own `__init__`. It now names `plainsong-mcp` and
`python -m plainsong_mcp`, both of which were run to confirm they work.

## Unreleased

### The compiler comes from PyPI, and the duplicated analysis is gone

`plainsong` 1.1.0 is published, so the dependency is a version specifier rather
than a git URL:

```toml
dependencies = ["plainsong>=1.1.0"]
```

1.1.0 is the first release carrying `plainsong.features`, so the floor is a real
requirement rather than caution: below it the install succeeds and the import
fails.

`plainsong_mcp/features.py` was **300 lines duplicated byte for byte** with
`plainsong/features.py` — the exact drift the repository split was meant to end,
sitting in plain sight in both trees. Per-bar analysis is a fact about music
rather than about MCP, so it belongs to the compiler. It lives there now and this
module re-exports it.

Nothing that used it had to change. `plainsong_mcp.features` still imports, and
returns the same objects: `features.BarFeatures is plainsong.features.BarFeatures`
is `True`. All 91 tests pass against the PyPI release.

## 1.0.0

Extracted from `plainsong`, where it grew up as `plainsong/mcp/`. The
compiler and the agent substrate are different products with different
audiences, so they are now different repositories.

- A Model Context Protocol server over stdio and loopback HTTP. Correct
  JSON-RPC 2.0: notifications draw no response, unknown methods give -32601,
  malformed input gives -32700, and a failing tool returns `isError` rather
  than a protocol error.
- 27 tools, enumerated from the compiler's own registry rather than maintained
  twice, so a tool added there appears here automatically.
- Ensemble sessions: several agents on one score, a voice each, optimistic
  concurrency with rebase-on-conflict, atomic writes and a shared log.
- `analyze_features` computes the sixteen per-bar features fleet-jepa-midi
  perceives.

Fixed on extraction: the notation-reference resource resolved its path by
walking up from its own file, which silently depended on this package sitting
inside `plainsong/`. It now asks the installed package where it lives.
