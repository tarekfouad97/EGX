import json
import os
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from egx_swing import ai_review, report
from egx_swing.setups import scan

from tests.test_setups import RISK_ON, base


def verdict(v="CONFIRM", **kw):
    d = {"verdict": v, "confidence": "medium", "summary": f"{v} summary", "news": [
        {"date": "2026-10-01", "headline": "Results up", "source": "Zawya", "url": "https://x/1", "impact": "positive"}],
        "upcoming_events": [], "fundamentals_view": "fine", "risks": []}
    d.update(kw)
    return d


def resp(data=None, stop="end_turn", text=None):
    body = text if text is not None else json.dumps(data)
    return NS(stop_reason=stop, content=[NS(type="text", text=body)], stop_details=None)


class FakeClient:
    """Mimics client.beta.messages.create; `script` maps symbol -> list of responses/exceptions."""

    def __init__(self, script):
        self.script, self.calls = script, []
        self.beta = NS(messages=NS(create=self.create))

    def create(self, **kw):
        self.calls.append(kw)
        sym = next(s for s in self.script if f"EGX: {s})" in kw["messages"][0]["content"])
        r = self.script[sym].pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def picks(*symbols, **kw):
    stocks = [base(symbol=s, **kw) for s in symbols]
    return scan(stocks, RISK_ON), {s["symbol"]: s for s in stocks}


def run(script, *symbols, **kw):
    res, by = picks(*symbols, **kw)
    events = []
    client = FakeClient(script)
    ai_review.apply(res, by, "2026-10-07", lambda *a: events.append(a), client=client)
    return res, events, client


class Verdicts(unittest.TestCase):
    def test_confirm_keeps_pick_unchanged(self):
        before = picks("AAA")[0]["signals"][0]["quality"]
        res, _, _ = run({"AAA": [resp(verdict("CONFIRM"))]}, "AAA")
        s = res["signals"][0]
        self.assertEqual(s["ai"]["verdict"], "CONFIRM")
        self.assertEqual(s["quality"], before)

    def test_caution_demotes_and_warns(self):
        before = picks("AAA")[0]["signals"][0]["quality"]
        res, _, _ = run({"AAA": [resp(verdict("CAUTION"))]}, "AAA")
        s = res["signals"][0]
        self.assertEqual(s["quality"], before - 10)
        self.assertTrue(any(w.startswith("AI review: CAUTION") for w in s["warnings"]))

    def test_avoid_moves_pick_to_vetoed(self):
        res, _, _ = run({"AAA": [resp(verdict("AVOID"))], "BBB": [resp(verdict("CONFIRM"))]}, "AAA", "BBB")
        self.assertEqual([s["symbol"] for s in res["signals"]], ["BBB"])
        self.assertEqual([s["symbol"] for s in res["vetoed"]], ["AAA"])

    def test_ai_never_improves_rank(self):
        res, _, _ = run({"AAA": [resp(verdict("CONFIRM"))], "BBB": [resp(verdict("CONFIRM"))]},
                        "AAA", "BBB")
        base_q = picks("AAA", "BBB")[0]["signals"]
        self.assertEqual([s["quality"] for s in res["signals"]], [s["quality"] for s in base_q])


class Failures(unittest.TestCase):
    def test_one_failure_does_not_affect_others(self):
        res, events, _ = run({"AAA": [RuntimeError("boom")], "BBB": [resp(verdict("CAUTION"))]}, "AAA", "BBB")
        by = {s["symbol"]: s for s in res["signals"]}
        self.assertIn("unavailable", by["AAA"]["ai"]["status"])
        self.assertIn("AI review unavailable - check news manually", by["AAA"]["warnings"])
        self.assertEqual(by["BBB"]["ai"]["verdict"], "CAUTION")
        self.assertEqual(events[-1][1], "PARTIAL")

    def test_refusal_is_a_failure_not_a_verdict(self):
        res, _, _ = run({"AAA": [resp(stop="refusal", text="")]}, "AAA")
        self.assertIn("declined", res["signals"][0]["ai"]["status"])

    def test_invalid_json_is_a_failure(self):
        res, _, _ = run({"AAA": [resp(text="not json")]}, "AAA")
        self.assertIn("unavailable", res["signals"][0]["ai"]["status"])

    def test_invalid_verdict_is_a_failure(self):
        res, _, _ = run({"AAA": [resp(verdict("BUY"))]}, "AAA")
        self.assertIn("invalid verdict", res["signals"][0]["ai"]["status"])

    def test_pause_turn_is_resumed(self):
        paused = NS(stop_reason="pause_turn", content=[NS(type="server_tool_use")], stop_details=None)
        res, _, client = run({"AAA": [paused, resp(verdict("CONFIRM"))]}, "AAA")
        self.assertEqual(res["signals"][0]["ai"]["verdict"], "CONFIRM")
        self.assertEqual(len(client.calls), 2)
        self.assertEqual(client.calls[1]["messages"][1]["role"], "assistant")

    def test_skipped_without_key(self):
        res, by = picks("AAA")
        with mock.patch.dict(os.environ, {}, clear=True):
            ai_review.apply(res, by, "2026-10-07", lambda *a: None)
        self.assertIn("ANTHROPIC_API_KEY not set", res["ai_review"])
        self.assertEqual(len(res["signals"]), 1)

    def test_disabled(self):
        res, by = picks("AAA")
        ai_review.apply(res, by, "2026-10-07", lambda *a: None, client=FakeClient({}), enabled=False)
        self.assertEqual(res["ai_review"], "disabled (--no-ai)")

    def test_review_limit(self):
        res, _, client = run({"AAA": [resp(verdict())], "BBB": [resp(verdict())]}, "AAA", "BBB")
        res2, by = picks("AAA", "BBB")
        c = FakeClient({"AAA": [resp(verdict())], "BBB": [resp(verdict())]})
        ai_review.apply(res2, by, "2026-10-07", lambda *a: None, client=c, max_reviews=1)
        self.assertEqual(len(c.calls), 1)
        self.assertEqual(sum(s["ai"]["status"] == "not reviewed (limit)" for s in res2["signals"]), 1)


class Request(unittest.TestCase):
    def test_request_shape(self):
        _, _, client = run({"AAA": [resp(verdict())]}, "AAA")
        kw = client.calls[0]
        self.assertEqual(kw["model"], "claude-opus-5-5")
        self.assertEqual(kw["tools"][0]["type"], "web_search_20260209")
        self.assertEqual(kw["output_config"]["format"]["schema"], ai_review.REVIEW_SCHEMA)
        self.assertEqual(kw["fallbacks"], "default")
        self.assertNotIn("thinking", kw)


class Fundamentals(unittest.TestCase):
    def test_loss_making_warns(self):
        self.assertEqual(ai_review.fundamental_warnings({"eps": -1.0}, "2026-10-07"),
                         ["Loss-making (negative EPS/ROE/net income)"])

    def test_earnings_inside_window(self):
        w = ai_review.fundamental_warnings({"next_earnings": "2026-10-20"}, "2026-10-07")
        self.assertIn("inside the holding window", w[0])
        self.assertEqual(ai_review.fundamental_warnings({"next_earnings": "2026-11-20"}, "2026-10-07"), [])

    def test_unix_earnings_date_converted(self):
        self.assertEqual(ai_review.fundamentals_of({"next_earnings": 1793188800})["next_earnings"], "2026-10-28")

    def test_warning_lowers_quality(self):
        res, by = picks("AAA", eps=-2.0)
        q = res["signals"][0]["quality"]
        ai_review.apply(res, by, "2026-10-07", lambda *a: None, enabled=False)
        self.assertEqual(res["signals"][0]["quality"], q - 5)


class Rendering(unittest.TestCase):
    def test_report_shows_verdict_news_and_vetoes(self):
        res, _, _ = run({"AAA": [resp(verdict("CONFIRM"))], "BBB": [resp(verdict("AVOID", summary="Suspended"))]},
                        "AAA", "BBB")
        res.update(run_status="OK", as_of="2026-10-07")
        md = report.render(res, RISK_ON, "now")
        self.assertIn("**AI review: CONFIRM**", md)
        self.assertIn("[Results up](https://x/1)", md)
        self.assertIn("## Vetoed by AI review (do not trade)", md)
        self.assertIn("Suspended", md)


if __name__ == "__main__":
    unittest.main()
