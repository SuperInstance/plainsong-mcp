"""The perception instruments: trace, custom dimensions, and the channel audit.

The seam the pulse-eye experiment found runs between the pulse and the bar,
as a change of *summary*: everything the loop needed was in the per-bar
stream, and the summaries averaged it away. These tests hold the three tools
that exist to keep that from happening again -- and, because two of them sit
on a compiler capability that is not in a release yet, they test both sides
of that gate.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from plainsong.agent.tools import Sandbox, ToolRegistry
from plainsong.runtime.config import load_config

from plainsong_mcp import features, perception, tools
from plainsong_mcp.protocol import Dispatcher  # noqa: F401  (imported shape, as test_mcp)
from plainsong_mcp.server import Server

try:  # the capability dimension_stats serves, present only on newer compilers
    from plainsong.features import annotation_stats as _CAPABILITY  # noqa: F401

    HAS_ANNOTATION_ROWS = True
except ImportError:
    HAS_ANNOTATION_ROWS = False

NOTATION = """**TRACK: Perception Sample**
[MetaData]
key: Am | tempo: 96 | swing: 0% | subdivision: 8th
time: 4/4

[A] (Verse - 4 Bars)
Melody: | A4 . C5 E5 | F4 . A4 C5 | A4 . E5 C5 | G4 A4 B4 C5 |
@bass | a1 . e2 . | f1 . c2 . | a1 e2 f2 g2 | a1 . . . |
"""

MELODY_PART = (
    "[A]\nMelody: | A4 . C5 E5 | F4 . A4 C5 | A4 . E5 C5 | G4 A4 B4 C5 |\n"
)
BREATH_PART = (
    "[A]\nMelody: | A4 . C5 E5 | F4 . A4 C5 |\nBreath: | 0.6 . . . | 0.2 . . . |\n"
)
BASS_PART = "[A]\n@bass | a1 . e2 . | f1 . c2 . | a1 e2 f2 g2 | a1 . . . |\n"


def message(method: str, params: dict | None = None, identifier: int | None = 1) -> str:
    payload: dict = {"jsonrpc": "2.0", "method": method}
    if identifier is not None:
        payload["id"] = identifier
    if params is not None:
        payload["params"] = params
    return json.dumps(payload)


class Client:
    """An in-process client, as in test_mcp: the wire format is under test too."""

    def __init__(self, server: Server) -> None:
        self.server = server
        self.next_id = 0

    def call(self, name: str, **arguments) -> object:
        self.next_id += 1
        answer = self.server.handle_text(
            message("tools/call", {"name": name, "arguments": arguments}, self.next_id)
        )
        assert answer is not None, f"{name} was not answered"
        result = json.loads(answer)["result"]
        assert "error" not in result, result
        if result.get("isError"):
            return result["content"][0]["text"]
        return result.get("structuredContent", result["content"][0]["text"])


def build_server(directory: Path) -> Server:
    config = load_config()
    registry = ToolRegistry(sandbox=Sandbox(root=directory / "work"), config=config)
    return Server(config=config, registry=registry, session_root=directory / "sessions")


class SessionCase(unittest.TestCase):
    """A server with one four-bar, two-voice session already written."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.client = Client(build_server(Path(self.temporary.name)))
        self.client.call("ensemble_open", session="probe", key="Am", tempo=96, bars=4)
        for voice, part in (("melody", MELODY_PART), ("bass", BASS_PART)):
            self.client.call(
                "ensemble_write_part",
                session="probe",
                voice=voice,
                agent="tester",
                content=part,
                base_version=0,
                summary="fixture",
            )


class TestPerceptionTrace(SessionCase):
    def test_the_trace_is_per_bar_and_never_only_a_mean(self) -> None:
        trace = self.client.call("perception_trace", session="probe")
        self.assertEqual(len(trace["per_bar"]), 4)
        for row in trace["per_bar"]:
            self.assertEqual(len(row["features"]), 16)
            self.assertEqual(len(row["vector"]), 16)
        self.assertNotIn("mean", trace, "the trace must not carry the summary it exists to bypass")

    def test_a_window_and_a_voice_can_be_traced_alone(self) -> None:
        window = self.client.call("perception_trace", session="probe", voice="bass", bars="2-3")
        self.assertEqual(window["voice"], "bass")
        self.assertEqual([row["bar"] for row in window["per_bar"]], [2, 3])
        self.assertEqual(window["bars"], {"total": 4, "from": 2, "to": 3})

    def test_a_fixed_width_table_is_available_for_reading(self) -> None:
        trace = self.client.call("perception_trace", session="probe", table=True)
        self.assertIn("note_d", trace["table"])  # headers are truncated to width 6
        self.assertEqual(len(trace["table"].strip().splitlines()), 5)  # header + 4 bars

    def test_a_session_that_does_not_exist_is_a_readable_error(self) -> None:
        answer = self.client.call("perception_trace", session="nowhere")
        self.assertTrue(isinstance(answer, str) and answer.startswith("error:"))


class TestAnalyzeFeaturesKeepsItsRows(SessionCase):
    """The seam was consumers collapsing early, not the data being hidden.

    ``analyze_features`` already returned the per-bar rows alongside the
    mean; this test pins that, so the summary cannot quietly become the only
    thing on the wire again.
    """

    def test_both_the_rows_and_the_mean_come_back(self) -> None:
        report = self.client.call("analyze_features", session="probe")
        self.assertEqual(len(report["per_bar"]), 4)
        self.assertIn("mean", report)
        self.assertEqual(len(report["feature_names"]), 16)


class TestPerceptionAudit(SessionCase):
    def test_every_channel_gets_a_verdict(self) -> None:
        audit = self.client.call("perception_audit", session="probe")
        self.assertEqual(len(audit["channels"]), 16)
        for name, channel in audit["channels"].items():
            self.assertIn(channel["verdict"], ("DEAD", "ALIVE", "COUPLED"), name)
            self.assertGreaterEqual(channel["variance"], 0.0)

    def test_channels_that_cannot_move_are_called_dead(self) -> None:
        # No chords are written and no bar rests: both channels are dials
        # connected to nothing, whatever else the fixture does.
        audit = self.client.call("perception_audit", session="probe")
        self.assertIn("chord_density", audit["dead"])
        self.assertIn("rest_ratio", audit["dead"])
        self.assertEqual(audit["channels"]["chord_density"]["verdict"], "DEAD")

    def test_coupled_channels_are_grouped_not_double_counted(self) -> None:
        audit = self.client.call("perception_audit", session="probe")
        for group in audit["coupled"]:
            self.assertGreater(len(group), 1)
            for name in group:
                self.assertEqual(audit["channels"][name]["verdict"], "COUPLED")
                self.assertTrue(set(audit["channels"][name]["coupled_with"]) <= set(group))
        for pair in audit["correlations"]:
            self.assertGreater(abs(pair["r"]), perception.COUPLING)
            self.assertLessEqual(abs(pair["r"]), 1.0)
        self.assertEqual(
            audit["steering_dimensions"],
            len(audit["independent"]) + len(audit["coupled"]),
        )

    def test_a_missing_session_is_a_readable_error(self) -> None:
        answer = self.client.call("perception_audit", session="nowhere")
        self.assertTrue(isinstance(answer, str) and answer.startswith("error:"))


class TestDimensionStats(SessionCase):
    def test_a_compiler_without_annotation_rows_gets_an_error_naming_them(self) -> None:
        # The gate itself, whichever side of it this install sits on: patch
        # the probe to the absent side and the tool must pass the message
        # through rather than fail or guess.
        missing = "error: this install of plainsong cannot see annotation rows"
        with mock.patch.object(tools, "_annotation_eye", return_value=(None, missing)):
            answer = self.client.call("dimension_stats", session="probe", row="Breath")
        self.assertEqual(answer, missing)

    @unittest.skipUnless(HAS_ANNOTATION_ROWS, "compiler does not publish annotation rows yet")
    def test_a_named_row_is_seen_with_its_per_bar_series(self) -> None:
        self.client.call(
            "ensemble_write_part",
            session="probe",
            voice="melody",
            agent="tester",
            content=BREATH_PART,
            base_version=2,
            summary="breath marks",
        )
        report = self.client.call("dimension_stats", session="probe", row="Breath")
        self.assertEqual(report["count"], 2)
        self.assertEqual(report["mean"], 0.4)
        self.assertEqual([(point["bar"], point["value"]) for point in report["per_bar"]], [(1, 0.6), (2, 0.2)])

    @unittest.skipUnless(HAS_ANNOTATION_ROWS, "compiler does not publish annotation rows yet")
    def test_an_unknown_row_lists_what_is_written(self) -> None:
        self.client.call(
            "ensemble_write_part",
            session="probe",
            voice="melody",
            agent="tester",
            content=BREATH_PART,
            base_version=2,
            summary="breath marks",
        )
        answer = self.client.call("dimension_stats", session="probe", row="Gaze")
        if isinstance(answer, str):  # a failed result arrives as text, not data
            answer = json.loads(answer)
        self.assertIn("error", answer)
        self.assertIn("Breath", answer["available_rows"])


def bar(values: dict[str, float], index: int = 1) -> features.BarFeatures:
    """A synthetic bar: every channel named, so the math is tested directly."""
    return features.BarFeatures(
        bar=index, start=float(index - 1) * 4.0, onsets=4,
        values={name: values.get(name, 0.0) for name in features.FEATURE_NAMES},
    )


class TestTheAuditMath(unittest.TestCase):
    """The verdicts on numbers built to make each one unavoidable."""

    def setUp(self) -> None:
        names = features.FEATURE_NAMES
        rising = [0.1, 0.2, 0.3, 0.4]
        self.bars = [
            bar({
                "note_density": rising[i],          # alive
                "avg_pitch": 2.0 * rising[i] + 1.0,  # coupled to note_density
                "velocity_std": 0.25,                # dead: never moves
                "syncopation": [0.9, 0.1, 0.8, 0.2][i],  # alive, uncorrelated
            }, i + 1)
            for i in range(4)
        ]
        self.assertEqual(len(names), 16)

    def test_pearson_reads_alignment_and_refuses_to_invent_it(self) -> None:
        self.assertAlmostEqual(perception.pearson([1, 2, 3], [2, 4, 6]), 1.0)
        self.assertAlmostEqual(perception.pearson([1, 2, 3], [6, 4, 2]), -1.0)
        self.assertIsNone(perception.pearson([1, 1, 1], [1, 2, 3]), "a dead series has no r")
        self.assertIsNone(perception.pearson([1.0], [1.0]))

    def test_dead_coupled_and_alive_verdicts(self) -> None:
        report = perception.audit({"(all)": self.bars})
        self.assertEqual(report["channels"]["syncopation"]["verdict"], "ALIVE")
        self.assertEqual(report["channels"]["velocity_std"]["verdict"], "DEAD")
        self.assertEqual(report["channels"]["note_density"]["verdict"], "COUPLED")
        self.assertEqual(report["channels"]["avg_pitch"]["verdict"], "COUPLED")
        self.assertEqual(report["coupled"], [["avg_pitch", "note_density"]])
        self.assertEqual(report["independent"], ["syncopation"])
        self.assertEqual(report["steering_dimensions"], 2)  # 16 channels, 14 dead, one merged pair

    def test_a_channel_dead_in_the_texture_but_alive_in_a_voice_is_alive(self) -> None:
        # Two voices moving in opposite directions cancel in the texture; the
        # channel is still steerable, and the audit must not bury it.
        cancelling = [bar({"syncopation": 0.5}, i + 1) for i in range(4)]
        one_voice = [
            bar({"syncopation": [0.9, 0.1, 0.8, 0.2][i]}, i + 1) for i in range(4)
        ]
        report = perception.audit({"(all)": cancelling, "violin1": one_voice})
        self.assertEqual(report["channels"]["syncopation"]["verdict"], "ALIVE")


if __name__ == "__main__":
    unittest.main()
