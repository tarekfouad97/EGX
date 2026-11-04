"""Tests for the Nov 2026 fixes: honest Stoch text, total-capital cap, intraday email flag,
input validation, and the history fallback order."""

import argparse
import unittest
from unittest import mock

from egx_swing import cli, fetch, notify, setups


def _pullback_stock(**over):
    s = {"symbol": "TEST", "currency": "EGP", "open": 10.0, "high": 10.3, "low": 10.0, "close": 10.2,
         "ema20": 10.1, "ema50": 9.8, "sma200": 9.0, "atr": 0.3, "rsi": 48.0,
         "stoch_k": 30.0, "stoch_d": 25.0, "adx": 22.0, "macd": 0.1, "macd_signal": 0.05,
         "vol_avg_10d": 2_000_000, "volume": 2_500_000, "perf_1m": 2.0}
    s.update(over)
    return s


class StochText(unittest.TestCase):
    def test_missing_previous_bar_is_not_called_rising(self):
        hit = setups.pullback(_pullback_stock())
        self.assertIsNotNone(hit)
        text = " ".join(hit["reasons"])
        self.assertIn("rising not verified", text)
        self.assertNotIn("and rising", text)

    def test_verified_rising(self):
        hit = setups.pullback(_pullback_stock(stoch_k_prev=27.0, stoch_d_prev=24.0))
        self.assertIn("and rising", " ".join(hit["reasons"]))

    def test_unverified_scores_lower(self):
        a = setups.pullback(_pullback_stock())["quality"]
        b = setups.pullback(_pullback_stock(stoch_k_prev=27.0, stoch_d_prev=24.0))["quality"]
        self.assertLess(a, b)


class CapitalCap(unittest.TestCase):
    def test_total_positions_never_exceed_capital(self):
        stocks = [_pullback_stock(symbol=f"S{i}", stoch_k_prev=27.0, stoch_d_prev=24.0) for i in range(30)]
        index = {"close": 100.0, "ema20": 95.0, "ema50": 90.0, "perf_1m": 1.0}
        res = setups.scan(stocks, index, {"capital": 20000.0, "risk_pct": 1.0, "strategy": "swing"})
        self.assertLessEqual(sum(s["position_egp"] for s in res["signals"]), 20000.0)
        self.assertTrue(res["over_budget"])


class IntradayEmail(unittest.TestCase):
    def test_subject_and_body_flag_intraday(self):
        rep = {"as_of": "2026-10-14", "run_status": "OK", "intraday": True, "signals": [],
               "regime": {"regime": "NEUTRAL", "note": ""}, "config": {"capital": 20000}}
        self.assertIn("INTRADAY", notify.subject(rep))
        self.assertIn("still open", notify.text_body(rep))

    def test_normal_run_not_flagged(self):
        rep = {"as_of": "2026-10-14", "run_status": "OK", "signals": [],
               "regime": {"regime": "NEUTRAL", "note": ""}, "config": {"capital": 20000}}
        self.assertNotIn("INTRADAY", notify.subject(rep))


class InputValidation(unittest.TestCase):
    def _args(self, **kw):
        base = {"capital": 20000.0, "risk_pct": 1.0, "top": 500, "min_adv": 5e6}
        base.update(kw)
        return argparse.Namespace(**base)

    def test_typo_capital_rejected(self):
        self.assertTrue(cli.validate_args(self._args(capital=2000.0)))

    def test_defaults_ok(self):
        self.assertEqual(cli.validate_args(self._args()), [])

    def test_crazy_risk_rejected(self):
        self.assertTrue(cli.validate_args(self._args(risk_pct=10.0)))


class HistoryFallback(unittest.TestCase):
    def test_tradingview_first_then_yahoo(self):
        with mock.patch("egx_swing.tvhistory.fetch_one", side_effect=OSError("down")), \
             mock.patch.object(fetch, "_yahoo_history", return_value=["y"]) as y:
            self.assertEqual(fetch.fetch_history("COMI"), ["y"])
            y.assert_called_once()

    def test_tradingview_used_when_available(self):
        with mock.patch("egx_swing.tvhistory.fetch_one", return_value=["tv"]) as tv, \
             mock.patch.object(fetch, "_yahoo_history") as y:
            self.assertEqual(fetch.fetch_history(fetch.YAHOO_INDEX), ["tv"])
            self.assertEqual(tv.call_args[0][0], "EGX30")
            y.assert_not_called()


if __name__ == "__main__":
    unittest.main()
