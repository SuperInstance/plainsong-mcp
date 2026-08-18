"""Whether an HTTP `Host` header names this machine -- re-exported from the
compiler.

The HTTP transport refuses a request whose `Host` is not a loopback name. That
is the guard against DNS rebinding, and comparing `Origin` against `Host` does
not replace it: an attacker points `evil.example` at 127.0.0.1, and a page
served from that domain sends both headers reading `evil.example`. They match
perfectly. What gives the attack away is that a rebound request always carries
the attacker's hostname, so the name itself is the thing to check.

This was two copies of the same eight lines -- one here, one in the compiler's
web server -- and both carried the same two faults, because the copy was a
copy:

- `name.startswith("127.")` admits `127.evil.example`, which is a registrable
  domain and can be pointed at 127.0.0.1 -- so the string test meant to
  recognise the 127/8 block let the exact attack it exists to stop walk
  through. An address is parsed as an address now.

- `[::1]:8765` and `[::1]` are both valid `Host` values for a loopback IPv6
  caller; the second is what a client sends when the port is the default.
  Stripping the port with `rsplit(":", 1)` before removing the brackets turned
  the second into `":"`, so a local caller was refused. The brackets are what
  separate an IPv6 address from its port, and have to be read first.

Whether a name is loopback is a fact about networking rather than about MCP,
so it moved beside `runtime/paths.py` in the compiler, the way the per-bar
analysis in `features.py` moved beside `notation/` and `perform/`. It lives
there now as `plainsong.runtime.localhost`, and `plainsong` 1.4.0 is the first
release that publishes it.

This module remains as a re-export rather than being deleted, because
`plainsong_mcp.localhost` is imported by `server.py` and by the test suite: a
name that already works should keep working. The code now exists once, which
was the point -- `plainsong_mcp.localhost.host_is_local` is
`plainsong.runtime.localhost.host_is_local`, so the two cannot drift while
both names exist.
"""

from __future__ import annotations

from plainsong.runtime.localhost import (
    LOOPBACK_NAMES,
    bind_is_loopback,
    host_is_local,
    hostname_of,
)

__all__ = [
    "LOOPBACK_NAMES",
    "bind_is_loopback",
    "host_is_local",
    "hostname_of",
]
