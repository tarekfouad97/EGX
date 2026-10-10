import json
import math
import os
import tempfile
import types
import unittest
from datetime import date, datetime, timedelta, timezone

from egx_swing import indicators, report
from egx_swing.pipeline import DROPPED, READY, RECOVERED, REQUIRED, Run
from egx_swing.setups import DEFAULTS

SESSION = date(2026, 10, 7)


def candles(n=260, end=SESSION, start=100.0, drift=0.002):
    """Synthetic EGX sessions (Sun-Thu) ending on `end`, gently trending with a wave."""
    days, d = [], end
    while len(days) < n:
        if d.weekday() not in (4, 5):          # skip Fri/Sat
            days.append(d)
        d -= timedelta(days=1)
    days.reverse()
    out = []
    for i, day in enumerate(days):
        c = start * (1 + drift) ** i * (1 + 0.03 * math.sin(i / 4))
        out.append({"date": day, "open": c * 0.995, "high": c * 1.01, "low": c * 0.99, "close": c,
                    "volume": 1_000_000 + 10_000 * (i % 7)})
    return out


def tv_row(symbol, **kw):
    """A complete screener row built from the same synthetic history."""
    row = indicators.compute(candles())
    row.pop("bar_date")
    ts = datetime(2026, 10, 7, 11, 30, tzinfo=timezone.utc).timestamp()
    row.update(symbol=symbol, name=symbol, sector="Finance", currency="EGP", pricescale=100,
               update_time=ts)
    row.update(kw)
    return row


def fake_fetch(universe=None, index=None, history=None):
    def fail(*a, **k):
        raise OSError("simulated outage")

    def hist(sym):
        h = (history or {}).get(sym)
        if h is None:
            raise OSError("404")
        return h

    return types.SimpleNamespace(
        fetch_universe=(lambda top: universe) if universe is not None else fail,
        fetch_index=(lambda: index) if index is not None else fail,
        fetch_history=hist, YAHOO_INDEX="^CASE30")


INDEX = {"close": 110, "ema20": 105, "ema50": 100, "perf_1m": 0.0}


def run(fetch, cache=None):
    r = Run(fetch=fetch, cache_path=cache, sleep=lambda s: None, workers=2, ai=False)   # never call the API
    return r.run(100, dict(DEFAULTS))


class Indicators(unittest.TestCase):
    def test_short_history_is_none(self):
        self.assertIsNone(indicators.compute(candles(100)))

    def test_all_required_present(self):
        ind = indicators.compute(candles())
        self.assertEqual([k for k in REQUIRED if ind.get(k) is None], [])
        self.assertEqual(ind["bar_date"], SESSION.isoformat())

    def test_rsi_extremes(self):
        up = [float(i) for i in range(1, 40)]
        self.assertEqual(indicators.rsi(up)[-1], 100.0)
        self.assertLess(indicators.rsi(up[::-1])[-1], 1.0)

    def test_sma_ema(self):
        xs = [1.0, 2.0, 3.0, 4.0]
        self.assertEqual(indicators.sma(xs, 2)[-1], 3.5)
        self.assertEqual(indicators.ema([5.0] * 30, 10)[-1], 5.0)

    def test_stoch_d_is_sma3_of_k(self):
        c = candles()
        k, d = indicators.stoch([x["high"] for x in c], [x["low"] for x in c], [x["close"] for x in c])
        self.assertAlmostEqual(d[-1], sum(k[-3:]) / 3)

    def test_perf_1m_uses_close_before_same_day_last_month(self):
        c = candles()
        ref = [x["close"] for x in c if x["date"] < date(2026, 9, 7)][-1]
        self.assertAlmostEqual(indicators.compute(c)["perf_1m"], (c[-1]["close"] / ref - 1) * 100)


class Pipeline(unittest.TestCase):
    def test_happy_path(self):
        res, _ = run(fake_fetch(universe=[tv_row("AAA")], index=INDEX, history={"AAA": candles()}))
        self.assertEqual(res["run_status"], "OK")
        self.assertEqual(res["data_status"]["AAA"]["state"], READY)
        self.assertEqual(res["as_of"], "2026-10-07")

    def test_missing_field_recovered_from_fallback(self):
        res, _ = run(fake_fetch(universe=[tv_row("AAA", sma200=None)], index=INDEX,
                                history={"AAA": candles()}))
        st = res["data_status"]["AAA"]
        self.assertEqual(st["state"], RECOVERED)
        self.assertIn("sma200", st["reason"])
        self.assertEqual(res["run_status"], "DEGRADED")

    def test_missing_field_and_no_fallback_is_dropped(self):
        res, _ = run(fake_fetch(universe=[tv_row("AAA", sma200=None), tv_row("BBB")], index=INDEX))
        self.assertEqual(res["data_status"]["AAA"]["state"], DROPPED)
        self.assertIn("fallback fetch failed", res["data_status"]["AAA"]["reason"])
        self.assertEqual(res["data_status"]["BBB"]["state"], READY)

    def test_stale_fallback_is_dropped(self):
        old = candles(end=date(2026, 9, 30))
        res, _ = run(fake_fetch(universe=[tv_row("AAA", rsi=None), tv_row("BBB")], index=INDEX,
                                history={"AAA": old}))
        self.assertEqual(res["data_status"]["AAA"]["state"], DROPPED)
        self.assertIn("also stale", res["data_status"]["AAA"]["reason"])

    def test_stale_screener_row_goes_to_recovery(self):
        stale_ts = datetime(2026, 9, 30, 11, 0, tzinfo=timezone.utc).timestamp()
        res, _ = run(fake_fetch(universe=[tv_row("AAA", update_time=stale_ts), tv_row("BBB")],
                                index=INDEX, history={"AAA": candles()}))
        self.assertEqual(res["data_status"]["AAA"]["state"], RECOVERED)
        self.assertIn("stale bar 2026-09-30", res["data_status"]["AAA"]["reason"])

    def test_screener_down_uses_cache_and_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            cache = os.path.join(d, "universe.json")
            with open(cache, "w") as f:
                json.dump([{"symbol": "AAA", "name": "A", "sector": "Finance", "currency": "EGP",
                            "pricescale": 100}], f)
            res, idx = run(fake_fetch(history={"AAA": candles()}), cache=cache)
        self.assertEqual(res["data_status"]["AAA"]["state"], RECOVERED)
        self.assertEqual(res["as_of"], "2026-10-07")
        self.assertEqual(res["regime"]["regime"], "UNKNOWN")
        self.assertEqual(res["run_status"], "DEGRADED")

    def test_successful_run_writes_cache(self):
        with tempfile.TemporaryDirectory() as d:
            cache = os.path.join(d, "sub", "universe.json")
            run(fake_fetch(universe=[tv_row("AAA")], index=INDEX), cache=cache)
            with open(cache) as f:
                self.assertEqual(json.load(f)[0]["symbol"], "AAA")

    def test_everything_down_still_reports(self):
        res, idx = run(fake_fetch())
        self.assertEqual(res["run_status"], "FAILED")
        self.assertEqual(res["signals"], [])
        md = report.render(res, idx, "now")
        self.assertIn("no trades", md)
        self.assertIn("UNIVERSE | FAILED", md)

    def test_scan_crash_still_reports(self):
        from egx_swing import pipeline
        orig, calls = pipeline.scan, []

        def flaky(stocks, index, cfg):
            calls.append(1)
            if len(calls) == 1:
                raise ZeroDivisionError("bug")
            return orig(stocks, index, cfg)
        pipeline.scan = flaky
        try:
            res, idx = run(fake_fetch(universe=[tv_row("AAA")], index=INDEX))
        finally:
            pipeline.scan = orig
        self.assertEqual(res["signals"], [])
        self.assertTrue(any(e["stage"] == "SCAN" and e["outcome"] == "FAILED" for e in res["events"]))
        self.assertIn("SCAN | FAILED", report.render(res, idx, "now"))

    def test_enrich_adds_previous_stoch_from_history(self):
        row = tv_row("AAA")
        row.pop("stoch_k_prev"), row.pop("stoch_d_prev")
        r = Run(fetch=fake_fetch(history={"AAA": candles()}), sleep=lambda s: None)
        from egx_swing import pipeline
        orig = pipeline.pullback
        pipeline.pullback = lambda s: True          # force candidacy
        try:
            r.enrich([row], "2026-10-07")
        finally:
            pipeline.pullback = orig
        self.assertIsNotNone(row.get("stoch_k_prev"))


if __name__ == "__main__":
    unittest.main()
