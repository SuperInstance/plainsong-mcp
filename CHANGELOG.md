# Changelog

## 1.0.0

Extracted from `tapscript-studio`, where it grew up as `tapscript/mcp/`. The
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
inside `tapscript/`. It now asks the installed package where it lives.
