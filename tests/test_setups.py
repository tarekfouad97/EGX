import unittest

from egx_swing.setups import DEFAULTS, bounce, breakout, market_regime, plan_trade, pullback, scan


def base(**kw):
    s = {
        "symbol": "TEST", "name": "Test Co", "sector": "Finance",
        "open": 99.0, "high": 101.0, "low": 98.0, "close": 100.0,
        "ema10": 100.0, "ema20": 99.0, "ema50": 95.0, "sma200": 85.0,
        "rsi": 48.0, "rsi_prev": 45.0, "stoch_k": 40.0, "stoch_d": 30.0,
        "macd": 1.0, "macd_signal": 0.5, "adx": 25.0, "di_plus": 25.0, "di_minus": 15.0,
        "bb_upper": 108.0, "bb_lower": 92.0, "atr": 3.0,
        "high_1m": 110.0, "low_1m": 92.0, "high_52w": 130.0, "low_52w": 70.0,
        "volume": 100_000, "vol_avg_10d": 100_000, "perf_1m": 2.0,
    }
    s.update(kw)
    return s


RISK_ON = {"close": 110, "ema20": 105, "ema50": 100, "perf_1m": 0.0}
RISK_OFF = {"close": 90, "ema20": 95, "ema50": 100, "perf_1m": -5.0}


class Regime(unittest.TestCase):
    def test_states(self):
        self.assertEqual(market_regime(RISK_ON)["regime"], "RISK-ON")
        self.assertEqual(market_regime(RISK_OFF)["regime"], "RISK-OFF")
        self.assertEqual(market_regime({})["regime"], "UNKNOWN")


class Setups(unittest.TestCase):
    def test_pullback_hits(self):
        self.assertEqual(pullback(base())["setup"], "PULLBACK")

    def test_pullback_needs_uptrend(self):
        self.assertIsNone(pullback(base(close=80.0, low=79.0)))

    def test_pullback_needs_stoch_turn(self):
        self.assertIsNone(pullback(base(stoch_k=25.0, stoch_d=30.0)))

    def test_breakout_hits(self):
        s = base(close=110.0, high=111.0, high_1m=110.5, rsi=65.0, volume=200_000)
        self.assertEqual(breakout(s)["setup"], "BREAKOUT")

    def test_breakout_needs_volume(self):
        s = base(close=110.0, high=111.0, high_1m=110.5, rsi=65.0, volume=120_000)
        self.assertIsNone(breakout(s))

    def test_bounce_hits(self):
        s = base(close=91.0, open=90.0, low=89.0, high=92.0, rsi=32.0, rsi_prev=28.0, ema20=99.0)
        self.assertEqual(bounce(s)["setup"], "BOUNCE")

    def test_bounce_needs_long_trend(self):
        s = base(close=91.0, low=89.0, rsi=32.0, rsi_prev=28.0, sma200=95.0)
        self.assertIsNone(bounce(s))

    def test_missing_data_is_not_a_signal(self):
        self.assertIsNone(pullback(base(rsi=None)))
        self.assertIsNone(breakout(base(volume=None)))
        self.assertIsNone(bounce(base(atr=None)))


class Plan(unittest.TestCase):
    def test_levels_and_size(self):
        s = base(adv_egp=1e9)
        p = plan_trade(s, pullback(s), dict(DEFAULTS))
        self.assertEqual(p["entry"], 101.3)                 # high + 0.1 ATR
        self.assertLess(p["stop"], p["entry"])
        self.assertAlmostEqual(p["rr_t1"], 1.5, places=1)
        self.assertLessEqual(p["risk_egp"], DEFAULTS["capital"] * DEFAULTS["risk_pct"] / 100)

    def test_regime_multiplier_halves_risk(self):
        s = base(adv_egp=1e9)
        full = plan_trade(s, pullback(s), dict(DEFAULTS), 1.0)
        half = plan_trade(s, pullback(s), dict(DEFAULTS), 0.5)
        self.assertAlmostEqual(half["shares"], full["shares"] / 2, delta=1)

    def test_liquidity_cap(self):
        s = base(adv_egp=50_000)                             # 10% of ADV = 5k EGP
        p = plan_trade(s, pullback(s), dict(DEFAULTS))
        self.assertLessEqual(p["position_egp"], 5_000)
        self.assertIn("Size capped by position/liquidity limit", p["warnings"])


class Scan(unittest.TestCase):
    def test_filters_illiquid(self):
        r = scan([base(vol_avg_10d=1_000)], RISK_ON)
        self.assertEqual(r["signals"], [])
        self.assertEqual(len(r["excluded"]), 1)

    def test_breakouts_suppressed_when_risk_off(self):
        s = base(close=110.0, high=111.0, high_1m=110.5, rsi=65.0, volume=200_000)
        self.assertEqual(scan([dict(s)], RISK_ON)["signals"][0]["setup"], "BREAKOUT")
        self.assertEqual(scan([dict(s)], RISK_OFF)["signals"], [])

    def test_ranked_by_quality(self):
        weak = base(symbol="WEAK", perf_1m=-10.0)
        strong = base(symbol="STRONG", perf_1m=10.0)
        sig = scan([weak, strong], RISK_ON)["signals"]
        self.assertEqual([x["symbol"] for x in sig], ["STRONG", "WEAK"])


if __name__ == "__main__":
    unittest.main()
