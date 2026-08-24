# Changelog

## Unreleased

### This repository can now cut a release

There was no release workflow at all. 1.0.0 reached PyPI by hand, and 1.0.1 has
been sitting tagged-in-name-only ever since -- the version bumped, the changelog
written, and nothing able to publish it.

`release.yml` now does what the sibling's does: a tag that must match the tree,
tests, a build, `twine check`, an idempotent publish and a GitHub Release. Two
things it carries that the sibling's does not, both because this repository has
already been bitten by them:

- **The version is read from `pyproject.toml`, not imported.** There is no
  `version.py` here and no `__version__`, so importing the package to ask its
  version would require installing it first, and the check would run after the
  build rather than before it.
- **No dependency may be a direct reference.** PyPI refuses a distribution whose
  metadata contains `name @ git+https://...`, and refuses it at upload -- after
  the tag exists and the build has passed. This repository has held exactly such
  a pin on `plainsong`. The guard fails in the first job instead, and it was
  checked against that real pin rather than assumed: it flags it.

**This still needs a Trusted Publisher configured on PyPI** before a tag will
publish. Without one the upload fails with `invalid-publisher: valid token, but
no corresponding publisher`, which is how the sibling accumulated five tags and
zero releases before anyone read the log. The workflow comment says exactly
which fields to set.

## 1.0.1 — 2026-08-18

`plainsong` 1.4.0 is published, and it carries `plainsong.runtime.localhost` --
the compiler's copy of the loopback check, which 1.0.0 shipped here as a real
implementation rather than a re-export, on the explicit understanding that it
would collapse the day the floor could be raised to the release carrying that
module. That day is today.

`plainsong_mcp/localhost.py` is now a re-export, the same move `features.py`
made in 1.0.0: `plainsong_mcp.localhost.host_is_local` is
`plainsong.runtime.localhost.host_is_local`, not merely a function that answers
the same way. `server.py` and the test suite import `plainsong_mcp.localhost`
exactly as before, so nothing that used it had to change. The two faults this
check exists to prevent -- `127.evil.example` passing `startswith("127.")`, and
`[::1]` losing its digits to a port-strip that ran before the brackets did --
cannot come back as a second local drift now, because there is only one
function object answering the question, not two copies of eight lines that
happen to agree today.

The dependency floor moves to match:

```toml
dependencies = ["plainsong>=1.4.0"]
```

1.1.0 remains a true floor for `features.py`; 1.4.0 is now the binding one, for
the same reason 1.1.0 was in 1.0.0 -- below it the install succeeds and the
import of `plainsong.runtime.localhost` fails.

`tests/test_localhost.py` loses the skip branch that used to guard against an
installed `plainsong` predating the module -- that branch is dead now that the
floor guarantees the module is there, and a dead skip is worse than no test, so
it was replaced rather than deleted. What replaced it asserts identity
(`assertIs`) instead of comparing answers case by case: the old test proved the
two copies agreed on the cases it thought to try, which is what "agrees with"
can ever mean about two separate implementations; the new one proves there is
only one implementation to disagree with itself, which is a stronger claim and
a shorter test. Every other test in that file is unchanged and still passes --
they now exercise the compiler's implementation through the re-export, which is
the point of a re-export.

## 1.0.0 — 2026-08-18

The first release. Everything below happened before it shipped, so it is
recorded rather than announced: nobody was running any of the code these
fixed.

### What it is

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

### The loopback check let a domain through, and mishandled IPv6

The rebinding guard added below required a loopback `Host`, and matched the
name with `name.startswith("127.")`. `127.evil.example` starts with those
characters, is registrable, and can be pointed at 127.0.0.1 — so the test meant
to recognise the 127/8 block admitted the exact attack the guard exists to
stop. An address is parsed as an address now.

The same lines read a bracketed IPv6 `Host` wrongly. The brackets are what
separate the address from the port, so stripping the port first turned `[::1]`
— which is what a client sends when the port is the default — into `":"`, and a
loopback caller was refused.

Both faults came over with the code, which was copied from the compiler's web
server; the compiler had them too and has fixed them the same way. The check
now lives in `plainsong_mcp/localhost.py` with `tests/test_localhost.py` on it,
and one of those tests compares this copy's answers against
`plainsong.runtime.localhost` case by case, so the two cannot drift while both
exist. **This file should become a re-export**, the way `features.py` did, as
soon as the `plainsong` floor in `pyproject.toml` can be raised to the release
carrying that module. It is inline for now because a security fix should not
wait on a release of a different package.

`bind_is_loopback` is separated from `host_is_local` in the same move: a
request addressed to `0.0.0.0` is legitimate, and a server *bound* to `0.0.0.0`
is what the "anyone who can reach this port" warning is for. They had been one
list answering both questions.

Two cases the original tests did not cover are covered now: a rebound `Host`
with **no `Origin` header at all** (a non-browser client omits it, so an
Origin-only guard has nothing to say — the `Host` check has to run first), and
`[::1]` with no port.

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
