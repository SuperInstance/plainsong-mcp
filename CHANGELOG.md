# Changelog

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
