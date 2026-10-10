import math
import unittest

from egx_swing.setups import (DEFAULTS, bounce, breakout, market_regime, plan_trade, pullback,
                              scan, screen, tick_size)


def base(**kw):
    """A stock that is a valid PULLBACK (and nothing else) unless overridden."""
    s = {
        "symbol": "TEST", "name": "Test Co", "sector": "Finance", "currency": "EGP", "pricescale": 100,
        "open": 99.0, "high": 101.0, "low": 98.0, "close": 100.0,
        "ema10": 100.0, "ema20": 99.0, "ema50": 95.0, "sma200": 85.0,
        "rsi": 48.0, "rsi_prev": 45.0, "stoch_k": 40.0, "stoch_d": 30.0,
        "stoch_k_prev": 25.0, "stoch_d_prev": 28.0,
        "macd": 1.0, "macd_signal": 0.5, "adx": 25.0, "di_plus": 25.0, "di_minus": 15.0,
        "bb_lower": 92.0, "atr": 3.0,
        "high_1m": 115.0, "high_52w": 130.0,
        "volume": 100_000, "vol_avg_10d": 100_000, "perf_1m": 2.0,
    }
    s.update(kw)
    return s


def brk(**kw):
    """A valid BREAKOUT."""
    d = dict(close=110.0, open=106.0, high=111.0, low=106.0, high_1m=110.5, rsi=65.0, volume=200_000,
             ema20=104.0, stoch_k=85.0, stoch_d=80.0)
    d.update(kw)
    return base(**d)


def bnc(**kw):
    """A valid BOUNCE."""
    d = dict(close=91.0, open=90.0, low=89.0, high=92.0, rsi=32.0, rsi_prev=28.0, ema20=99.0,
             stoch_k=15.0, stoch_d=10.0, bb_lower=90.0)
    d.update(kw)
    return base(**d)


RISK_ON = {"close": 110, "ema20": 105, "ema50": 100, "perf_1m": 0.0}
NEUTRAL = {"close": 102, "ema20": 99, "ema50": 100, "perf_1m": 0.0}
RISK_OFF = {"close": 90, "ema20": 95, "ema50": 100, "perf_1m": -5.0}
CFG = dict(DEFAULTS)


def plan(s, hit_fn=pullback, cfg=None, mult=1.0):
    s = {**s, "adv_egp": s["close"] * s["vol_avg_10d"]}
    return plan_trade(s, hit_fn(s), cfg or CFG, mult)


class Regime(unittest.TestCase):
    def test_states(self):
        self.assertEqual(market_regime(RISK_ON)["regime"], "RISK-ON")
        self.assertEqual(market_regime(NEUTRAL)["regime"], "NEUTRAL")
        self.assertEqual(market_regime(RISK_OFF)["regime"], "RISK-OFF")
        self.assertEqual(market_regime({})["regime"], "UNKNOWN")

    def test_risk_off_boundary(self):
        # close below EMA50 but EMA20 still above it -> NEUTRAL, not RISK-OFF
        self.assertEqual(market_regime({"close": 98, "ema20": 101, "ema50": 100})["regime"], "NEUTRAL")


class Pullback(unittest.TestCase):
    def test_hits(self):
        self.assertEqual(pullback(base())["setup"], "PULLBACK")

    def test_needs_price_above_sma200(self):
        self.assertIsNone(pullback(base(sma200=100.5, ema50=101.0, ema20=102.0, low=99.0)))

    def test_needs_ema_stack(self):
        self.assertIsNone(pullback(base(ema20=94.0, low=93.0)))       # EMA20 < EMA50
        self.assertIsNone(pullback(base(ema50=84.0)))                 # EMA50 < SMA200

    def test_needs_dip_to_ema20(self):
        self.assertIsNone(pullback(base(low=101.0, close=101.5)))     # low > EMA20 + 0.5 ATR

    def test_rejects_extended_close(self):
        self.assertIsNone(pullback(base(close=102.5, high=103.0)))    # close > EMA20 + 1 ATR

    def test_needs_rsi_reset(self):
        self.assertIsNone(pullback(base(rsi=62.0)))
        self.assertIsNone(pullback(base(rsi=35.0)))

    def test_needs_stoch_turn(self):
        self.assertIsNone(pullback(base(stoch_k=25.0, stoch_d=30.0)))  # K below D
        self.assertIsNone(pullback(base(stoch_k=65.0, stoch_d=50.0)))  # K too high
        self.assertIsNone(pullback(base(stoch_k_prev=45.0)))           # K falling

    def test_reason_distinguishes_fresh_cross(self):
        self.assertIn("crossed above", pullback(base())["reasons"][2])
        self.assertIn("rising", pullback(base(stoch_k_prev=35.0, stoch_d_prev=25.0))["reasons"][2])


class Breakout(unittest.TestCase):
    def test_hits(self):
        self.assertEqual(breakout(brk())["setup"], "BREAKOUT")

    def test_needs_1m_high(self):
        self.assertIsNone(breakout(brk(high_1m=113.0)))

    def test_needs_volume(self):
        self.assertIsNone(breakout(brk(volume=140_000)))

    def test_needs_trend(self):
        self.assertIsNone(breakout(brk(adx=18.0)))
        self.assertIsNone(breakout(brk(di_plus=10.0)))

    def test_needs_rsi_band(self):
        self.assertIsNone(breakout(brk(rsi=50.0)))
        self.assertIsNone(breakout(brk(rsi=80.0)))

    def test_stop_is_entry_minus_1_5_atr(self):
        p = plan(brk(), breakout)
        self.assertAlmostEqual(p["entry"] - p["stop"], 1.5 * 3.0, delta=0.011)


class Bounce(unittest.TestCase):
    def test_hits(self):
        self.assertEqual(bounce(bnc())["setup"], "BOUNCE")

    def test_needs_long_trend(self):
        self.assertIsNone(bounce(bnc(sma200=95.0)))

    def test_needs_oversold(self):
        self.assertIsNone(bounce(bnc(rsi=40.0, rsi_prev=38.0)))

    def test_needs_band_touch(self):
        self.assertIsNone(bounce(bnc(low=92.0, close=93.0)))

    def test_needs_turn(self):
        self.assertIsNone(bounce(bnc(rsi=30.0, rsi_prev=33.0, stoch_k=8.0, stoch_d=10.0)))

    def test_reason_honest_when_rsi_falling(self):
        hit = bounce(bnc(rsi=30.0, rsi_prev=33.0))
        self.assertIn("still falling", hit["reasons"][1])

    def test_t1_is_ema20_within_1_to_1_5r(self):
        p = plan(bnc(), bounce)                              # EMA20 99.0 is ~1.2R above entry
        self.assertEqual(p["t1"], 99.0)
        self.assertEqual(plan(bnc(ema20=93.0), bounce)["rr_t1"], 1.0)    # floored at 1R
        self.assertEqual(plan(bnc(ema20=120.0), bounce)["rr_t1"], 1.5)   # capped at 1.5R


class Robustness(unittest.TestCase):
    def test_missing_data_is_not_a_signal(self):
        self.assertIsNone(pullback(base(rsi=None)))
        self.assertIsNone(breakout(brk(volume=None)))
        self.assertIsNone(bounce(bnc(atr=None)))

    def test_missing_open_does_not_crash(self):
        self.assertEqual(len(scan([base(open=None)], RISK_ON)["signals"]), 1)
        self.assertEqual(len(scan([bnc(open=None)], RISK_ON)["signals"]), 1)

    def test_nan_is_rejected(self):
        r = scan([base(vol_avg_10d=math.nan)], RISK_ON)
        self.assertEqual(r["signals"], [])
        self.assertEqual(r["excluded"][0]["reason"], "missing data")

    def test_screen_does_not_mutate(self):
        s = base()
        screen(s, CFG)
        self.assertNotIn("adv_egp", s)


class Plan(unittest.TestCase):
    def test_levels_and_size(self):
        p = plan(base())
        self.assertEqual(p["entry"], 101.3)                 # high + 0.1 ATR
        self.assertLess(p["stop"], p["entry"])
        self.assertAlmostEqual(p["rr_t1"], 1.5, places=1)
        self.assertLessEqual(p["risk_egp"], CFG["capital"] * CFG["risk_pct"] / 100)

    def test_regime_multiplier_halves_risk(self):
        full, half = plan(base(), mult=1.0), plan(base(), mult=0.5)
        self.assertAlmostEqual(half["shares"], full["shares"] / 2, delta=1)

    def test_liquidity_cap(self):
        p = plan(base(vol_avg_10d=500))                      # ADV 50k -> 10% = 5k EGP
        self.assertLessEqual(p["position_egp"], 5_000)
        self.assertEqual(p["notes"], ["Size capped by liquidity limit"])

    def test_sub_1_egp_uses_0_001_tick(self):
        s = brk(close=0.271, open=0.26, high=0.272, low=0.26, high_1m=0.272, ema50=0.25, sma200=0.2,
                ema20=0.26, atr=0.01, pricescale=1000, vol_avg_10d=100_000_000, volume=200_000_000)
        self.assertEqual(tick_size(s), 0.001)
        p = plan(s, breakout)
        self.assertGreater(p["entry"], s["high"])
        self.assertEqual(p["entry"], 0.273)                  # 0.272 + 0.1 ATR on the 0.001 grid, not 0.27
        self.assertEqual(p["decimals"], 3)

    def test_entry_strictly_above_high(self):
        s = base(atr=0.01, high=100.0)                       # 0.1 ATR is below one tick
        p = plan_trade(s, {"setup": "PULLBACK", "stop_raw": 99.0}, CFG)
        self.assertEqual(p["entry"], 100.01)

    def test_breakout_gets_52w_resistance_warning(self):
        p = plan(brk(high_1m=110.0, high_52w=113.0), breakout)
        self.assertTrue(any("52W high" in w for w in p["warnings"]))

    def test_1m_resistance_warning(self):
        p = plan(base(high_1m=103.0))
        self.assertTrue(any("1M high" in w for w in p["warnings"]))

    def test_extended_warning(self):
        self.assertTrue(any("extended" in w for w in plan(base(perf_1m=30.0))["warnings"]))


class Scan(unittest.TestCase):
    def test_filters_illiquid(self):
        r = scan([base(vol_avg_10d=1_000)], RISK_ON)
        self.assertEqual(r["signals"], [])
        self.assertTrue(r["excluded"][0]["reason"].startswith("ADV"))

    def test_filters_atr_band(self):
        self.assertEqual(scan([base(atr=0.5)], RISK_ON)["signals"], [])     # 0.5% ATR
        self.assertEqual(scan([base(atr=9.0)], RISK_ON)["signals"], [])     # 9% ATR

    def test_excludes_usd_quoted(self):
        r = scan([base(currency="USD")], RISK_ON)
        self.assertEqual(r["signals"], [])
        self.assertIn("USD", r["excluded"][0]["reason"])

    def test_adv_reason_not_contradictory(self):
        r = scan([base(vol_avg_10d=23_000)], RISK_ON, {"min_adv_egp": 2_500_000})
        self.assertEqual(r["excluded"][0]["reason"], "ADV 2.3M EGP < 2.5M")

    def test_breakouts_suppressed_when_risk_off(self):
        self.assertEqual(scan([brk()], RISK_ON)["signals"][0]["setup"], "BREAKOUT")
        self.assertEqual(scan([brk()], RISK_OFF)["signals"], [])

    def test_ranked_by_quality(self):
        sig = scan([base(symbol="WEAK", perf_1m=-10.0), base(symbol="STRONG", perf_1m=10.0)], RISK_ON)["signals"]
        self.assertEqual([x["symbol"] for x in sig], ["STRONG", "WEAK"])

    def test_warning_lowers_quality(self):
        a = scan([base()], RISK_ON)["signals"][0]["quality"]
        b = scan([base(high_1m=103.0)], RISK_ON)["signals"][0]["quality"]
        self.assertEqual(a - b, 5)

    def test_size_cap_does_not_lower_quality(self):
        tight = base(symbol="TIGHT", low=99.5, ema50=98.0, atr=1.5)       # tight stop -> position cap
        r = scan([tight], RISK_ON)["signals"][0]
        self.assertTrue(r["notes"])
        self.assertEqual(r["warnings"], [])
        self.assertEqual(r["quality"], scan([tight], {**RISK_OFF, "perf_1m": 0.0})["signals"][0]["quality"])


if __name__ == "__main__":
    unittest.main()
