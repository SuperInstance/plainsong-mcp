# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An MCP server for TapScript. It serves the compiler's own tools over the Model
Context Protocol, and adds the one thing that is not in the compiler: an
*ensemble session*, where several agents write one score at the same time and
each owns a voice.

It depends on `SuperInstance/tapscript-studio` and that repository does not
depend on this one. Keep it that way. Anything that belongs to the compiler —
notation, arranging, rendering, the tool implementations themselves — goes
there; what lives here is the protocol, the two transports, and the session.

This repository was extracted from tapscript-studio rather than written fresh,
so `tapscript/mcp/` still exists over there. That copy is on its way out. Until
it goes, a fix made here has to be made there too, and vice versa — which is
exactly the drift the split was meant to end, so the sooner it goes the better.

## Commands

```bash
python3 -m unittest discover -s tests -v
python3 -m ruff check tapscript_mcp tests
python3 -m tapscript spec --tag mcp

# Drive the server by hand. This is how the protocol was verified.
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"x","version":"1"}}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | python3 -m tapscript_mcp

python3 -m tapscript_mcp --list-tools
python3 -m tapscript_mcp --http --port 8766
```

The tests import `tapscript`. In a checkout that has not installed it, put the
compiler on the path: `PYTHONPATH=../tapscript-studio python3 -m unittest ...`.

## The rules that carry over

Both are inherited from the compiler and both are load-bearing here too.

**Nothing may be imported at module scope outside the standard library.** CI
installs the compiler and nothing else. There is no MCP SDK in this repository
and there should not be: the protocol is a few hundred lines of JSON-RPC and a
dependency on an SDK would be a dependency the compiler itself refuses to have.

**Nothing may hardcode a path.** Session storage resolves through the
compiler's `runtime/paths.py`.

## The distinction the protocol turns on

A malformed request is a *protocol error* and gets an error object. A tool that
ran and could not do what was asked is a *result* with `isError` set. These are
not interchangeable. A model reading an error object concludes the server is
broken and gives up; reading a failed result, it reads the message and tries
something else. Only `RpcError` produces the former.

Related, and easy to get wrong the same way: the server does not decide whether
a tool failed by inspecting the text it returned. The registry knows whether it
could run the thing, and says so — `call_result` returns `(text, failed)`. Do
not reintroduce guessing from the string.

A notification — a message with no `id` — draws no response at all, not even an
error. A batch that produces only notifications writes nothing back.

Codes: `-32700` parse, `-32600` invalid request, `-32601` unknown method,
`-32602` invalid params, `-32603` internal, and MCP's own `-32002` for a URI
that resolves to nothing.

One known inconsistency, left deliberately: a parse error carrying no id gets an
answer, an invalid request carrying no id does not. Defensible — a request
without an id is a notification — but the two paths disagree, and if you touch
either, make them agree.

## The tool list is not written here

It is the compiler's `ToolRegistry.specs()`, which already emits JSON Schema. A
tool added anywhere in tapscript appears over the protocol with nothing in this
repository changing. Do not maintain a second list — that is the same "one of
everything" rule the compiler keeps, and the reason it keeps it.

## Ensemble sessions

The concurrency is the delicate part.

- Optimistic, not locked: every write carries the version it was read at, and a
  write against a stale version is **refused and handed the current state to
  rebase onto** rather than overwriting. The refusal is a result, not an error.
- Locks are held only around a read-modify-write of the manifest — never across
  a call to a model. A model call takes seconds; a lock held that long is a lock
  nobody else gets.
- The lock is `O_CREAT|O_EXCL`; writes land through `os.replace`, which is
  atomic. On Windows a file with a delete pending answers `PermissionError` on
  open, and acquisition treats that as contention rather than as an error.
- The merge is deterministic: the same set of parts produces byte-identical
  output whatever order they were written in. There is a test that proves it
  across three orders. If you change the merge, that test is the one to keep.
- A part is parsed before it is accepted, so invalid notation never lands, and
  the validator refuses a part that speaks for a voice other than its own.

"Ensemble" here always means the multi-agent session. What the compiler calls
`tapscript stage` — who hears what on a physical stage — is a different thing
that was briefly given the same name, and renaming it was worth doing.

## Specs

`specs/mcp.toml` states the promises; the checks live in
`tapscript_mcp/selfcheck.py` and run under the compiler's `tapscript spec`
harness. A user runs them to find out what works on their machine. A new
capability wants a spec as well as a test.

## Rough edges

- No third-party MCP client has ever connected to this server. The protocol is
  verified by hand-driven JSON-RPC against the specification, which is strong
  evidence and not the same thing as Claude Desktop or an SDK client connecting.
  Doing that is the single most valuable unblocked piece of work here.
- The HTTP transport is loopback-first and refuses cross-origin requests. It
  warns loudly when bound anywhere else, because anyone who can reach the port
  can run every tool against the workspace.
- The dependency in `pyproject.toml` is pinned to a branch of tapscript-studio
  until that branch merges. See the comment there.
