"""Shared constants + MCP client for the Seamstress gate-1 walking skeleton.

gate1-features-v1 — the SIX tracked features, frozen before stitch 1
(spec §0.1 spirit: the measurement is a versioned object). Chosen by
discriminability: each has a real seed-vs-canon gap. Normalisation uses the
canon's pooled per-feature std (floor 0.03) so distances are in sigma units.
"""
import json, urllib.request

MCP_URL = "http://127.0.0.1:8765/"
SESSION = "seamstress-gate1"
CANON_DIR = "canon"

# frozen measurement object
FEATURES = [
    "note_density",      # seed 1.000  canon 0.414
    "syncopation",       # seed 0.000  canon 0.665
    "register_spread",   # seed 0.081  canon 0.139
    "rest_ratio",        # seed 0.000  canon 0.145
    "harmonic_tension",  # seed 0.558  canon 0.630
    "interval_size",     # seed 0.401  canon 0.479
]
STD_FLOOR = 0.03
# canon per-feature std observed at freeze time (gate1-canon-std-v1)
CANON_STD_FROZEN = {
    "note_density": 0.101, "syncopation": 0.185, "register_spread": 0.053,
    "rest_ratio": 0.100, "harmonic_tension": 0.070, "interval_size": 0.163,
}

def call(name, args, timeout=60):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                          "params": {"name": name, "arguments": args}}).encode()
    req = urllib.request.Request(MCP_URL, data=payload,
                                 headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    if resp.get("error"):
        raise RuntimeError(f"MCP error: {resp['error']}")
    return resp["result"]

def call_text(name, args, timeout=60):
    r = call(name, args, timeout)
    for c in r.get("content", []):
        if c.get("type") == "text":
            return c["text"]
    raise RuntimeError(f"no text content from {name}: {r}")

def analyze_mean(args):
    """analyze_features -> (mean dict over 16 features, full text json)."""
    txt = call_text("analyze_features", args)
    return json.loads(txt)

def vec6(mean):
    return [round(mean[f], 4) for f in FEATURES]
