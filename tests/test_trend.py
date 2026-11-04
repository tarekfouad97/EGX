"""Tests for the TREND setup (new 50-session high + trailing stop) and its email/report output."""

import unittest

from egx_swing import notify, report, setups


def _stock(**over):
    s = {"symbol": "TRND", "name": "Trend Co", "currency": "EGP", "open": 10.0, "high": 10.6, "low": 9.9,
         "close": 10.5, "ema20": 10.0, "ema50": 9.5, "sma200": 8.0, "atr": 0.3, "rsi": 65.0,
         "stoch_k": 80.0, "stoch_d": 70.0, "high_50_prev": 10.4, "high_1m": 10.6, "high_52w": 12.0,
         "vol_avg_10d": 2_000_000, "volume": 3_000_000, "perf_1m": 8.0}
    s.update(over)
    return s


IDX = {"close": 100.0, "ema20": 95.0, "ema50": 90.0, "perf_1m": 2.0}


class TrendRule(unittest.TestCase):
    def test_new_high_in_uptrend_fires(self):
        self.assertEqual(setups.trend(_stock())["setup"], "TREND")

    def test_below_prior_high_does_not_fire(self):
        self.assertIsNone(setups.trend(_stock(close=10.3)))

    def test_downtrend_does_not_fire(self):
        self.assertIsNone(setups.trend(_stock(ema50=7.5)))
        self.assertIsNone(setups.trend(_stock(sma200=11.0)))

    def test_missing_50_session_high_does_not_fire(self):
        self.assertIsNone(setups.trend(_stock(high_50_prev=None)))

    def test_plan_has_stop_2atr_and_no_targets(self):
        sig = setups.scan([_stock()], IDX)["signals"][0]
        self.assertEqual(sig["setup"], "TREND")
        self.assertIsNone(sig["t1"])
        self.assertEqual(sig["trail_atr"], setups.TRAIL_ATR)
        self.assertAlmostEqual(sig["entry"] - sig["stop"], 2 * 0.3, delta=0.02)

    def test_default_strategy_is_trend_and_swing_still_available(self):
        self.assertEqual(setups.DEFAULTS["strategy"], "trend")
        res = setups.scan([_stock()], IDX, {"strategy": "swing"})
        self.assertTrue(all(s["setup"] != "TREND" for s in res["signals"]))


class TrendOutput(unittest.TestCase):
    def _report(self):
        res = setups.scan([_stock()], IDX)
        res.update({"as_of": "2026-11-04", "run_status": "OK", "index": IDX})
        return res

    def test_email_says_trailing_stop_not_targets(self):
        body = notify.text_body(self._report())
        self.assertIn("No target: trail the stop", body)
        self.assertNotIn("Sell half", body)
        self.assertNotIn("Best case", body)
        notify.html_body(self._report())          # renders without error

    def test_report_renders(self):
        md = report.render(self._report(), IDX, None)
        self.assertIn("trail 3 ATR", md)


if __name__ == "__main__":
    unittest.main()
