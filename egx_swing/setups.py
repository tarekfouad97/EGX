"""Swing setup detection and trade planning.

Three long-only setups, each evaluated on the latest daily bar:

  PULLBACK  - established uptrend, price has dipped back to the 20 EMA and
              momentum is turning up again.
  BREAKOUT  - close at/through the 1-month high on expanding volume with a
              trending ADX.
  BOUNCE    - oversold reversal while the long-term (200 SMA) trend is intact.

Every candidate gets a buy-stop entry above today's high, an ATR-based stop,
two R-multiple targets, and a quality score used for ranking. All functions
are pure: they take dicts of indicator values and return new dicts.
"""

import math

DEFAULTS = {
    "min_adv_egp": 5_000_000,   # avg daily value traded floor
    "min_atr_pct": 1.0,         # too quiet to swing below this
    "max_atr_pct": 8.0,         # too wild to size sensibly above this
    "capital": 100_000,         # EGP
    "risk_pct": 1.0,            # % of capital risked per trade
    "max_position_pct": 25.0,   # cap on a single position's value
    "max_adv_pct": 10.0,        # never be more than this % of a day's value
}


def _num(*vals):
    return all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
               for v in vals)


def tick_size(s):
    """EGX price step: 0.01, or 0.001 for stocks priced under 1 EGP (TradingView pricescale)."""
    ps = s.get("pricescale")
    if _num(ps) and ps > 0:
        return 1 / ps
    return 0.001 if _num(s.get("close")) and s["close"] < 1 else 0.01


def _decimals(tick):
    return max(0, round(-math.log10(tick)))


def _to_tick(price, tick, how):
    steps = price / tick
    steps = {"up": math.ceil(steps - 1e-9), "down": math.floor(steps + 1e-9)}.get(how, round(steps))
    return round(steps * tick, _decimals(tick))


def entry_raw(s):
    """Buy-stop trigger before rounding: just above today's high."""
    return (s.get("high") if _num(s.get("high")) else s["close"]) + 0.1 * s["atr"]


# ───────────────────────────── market regime ──────────────────────────────

def market_regime(index):
    """RISK-ON / NEUTRAL / RISK-OFF from EGX30 vs its moving averages."""
    close, ema20, ema50 = index.get("close"), index.get("ema20"), index.get("ema50")
    if not _num(close, ema20, ema50):
        return {"regime": "UNKNOWN", "risk_mult": 0.5,
                "note": "EGX30 data unavailable - risk halved, breakouts suppressed"}
    if close > ema20 > ema50:
        return {"regime": "RISK-ON", "risk_mult": 1.0,
                "note": "EGX30 above rising 20/50 EMAs"}
    if close < ema50 and ema20 < ema50:
        return {"regime": "RISK-OFF", "risk_mult": 0.5,
                "note": "EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed"}
    return {"regime": "NEUTRAL", "risk_mult": 0.75,
            "note": "EGX30 mixed vs 20/50 EMAs - risk reduced to 75%"}


# ───────────────────────────── setups ─────────────────────────────────────

def pullback(s):
    c, e20, e50, sma200 = s.get("close"), s.get("ema20"), s.get("ema50"), s.get("sma200")
    atr, rsi, k, d = s.get("atr"), s.get("rsi"), s.get("stoch_k"), s.get("stoch_d")
    low = s.get("low")
    if not _num(c, e20, e50, sma200, atr, rsi, k, d, low):
        return None
    uptrend = c > sma200 and e20 > e50 > sma200
    near_ema = low <= e20 + 0.5 * atr and c >= e50 and c <= e20 + 1.0 * atr
    reset = 38 <= rsi <= 58
    k_prev, d_prev = s.get("stoch_k_prev"), s.get("stoch_d_prev")
    turning = k > d and k < 60 and (not _num(k_prev) or k > k_prev)
    if not (uptrend and near_ema and reset and turning):
        return None
    fresh = _num(k_prev, d_prev) and k_prev <= d_prev
    stoch = (f"Stoch %K {k:.0f} crossed above %D {d:.0f} today" if fresh
             else f"Stoch %K {k:.0f} above %D {d:.0f} and rising")
    reasons = [f"Uptrend: EMA20 {e20:.2f} > EMA50 {e50:.2f} > SMA200 {sma200:.2f}",
               f"Pulled back toward EMA20 {e20:.2f} (low {low:.2f})",
               f"RSI {rsi:.0f} reset, {stoch}"]
    quality = 50
    quality += 10 if s.get("adx") and s["adx"] > 20 else 0
    quality += 10 if _num(s.get("macd"), s.get("macd_signal")) and s["macd"] > s["macd_signal"] else 0
    quality += 10 if 42 <= rsi <= 52 else 0
    quality += 10 if _num(s.get("open")) and c > s["open"] else 0   # bullish candle
    quality += 5 if fresh else 0
    stop = min(low, e50) - 0.5 * atr
    return {"setup": "PULLBACK", "stop_raw": stop, "quality": quality, "reasons": reasons}


def breakout(s):
    c, h1m, e50, atr, rsi = s.get("close"), s.get("high_1m"), s.get("ema50"), s.get("atr"), s.get("rsi")
    vol, vavg = s.get("volume"), s.get("vol_avg_10d")
    adx, dip, dim = s.get("adx"), s.get("di_plus"), s.get("di_minus")
    if not _num(c, h1m, e50, atr, rsi, vol, vavg, adx, dip, dim) or vavg <= 0:
        return None
    rel_vol = vol / vavg
    at_high = c >= 0.99 * h1m
    trending = adx > 20 and dip > dim
    if not (at_high and rel_vol >= 1.5 and trending and 55 <= rsi <= 78 and c > e50):
        return None
    reasons = [f"Close {c:.2f} at 1M high {h1m:.2f}",
               f"Volume {rel_vol:.1f}x 10d avg",
               f"ADX {adx:.0f} with +DI {dip:.0f} > -DI {dim:.0f}, RSI {rsi:.0f}"]
    quality = 50
    quality += 10 if rel_vol >= 2.5 else 0
    quality += 10 if adx > 30 else 0
    quality += 10 if _num(s.get("sma200")) and c > s["sma200"] else 0
    quality += 10 if rsi <= 70 else -10                   # not already stretched
    stop = entry_raw(s) - 1.5 * atr
    return {"setup": "BREAKOUT", "stop_raw": stop, "quality": quality, "reasons": reasons}


def bounce(s):
    c, sma200, atr, rsi, rsi_prev = s.get("close"), s.get("sma200"), s.get("atr"), s.get("rsi"), s.get("rsi_prev")
    k, d, bbl, low = s.get("stoch_k"), s.get("stoch_d"), s.get("bb_lower"), s.get("low")
    if not _num(c, sma200, atr, rsi, rsi_prev, k, d, bbl, low):
        return None
    long_trend = c > sma200
    oversold = rsi < 35 or (rsi_prev < 30 and rsi > rsi_prev)
    at_band = low <= bbl * 1.01
    turning = k > d or rsi > rsi_prev
    if not (long_trend and oversold and at_band and turning):
        return None
    rsi_txt = (f"RSI {rsi:.0f} (prev {rsi_prev:.0f}) oversold and turning up" if rsi > rsi_prev
               else f"RSI {rsi:.0f} (prev {rsi_prev:.0f}) oversold, still falling; Stoch %K {k:.0f} > %D {d:.0f}")
    band_txt = (f"Low {low:.2f} pierced lower Bollinger band {bbl:.2f}" if low <= bbl
                else f"Low {low:.2f} within 1% of lower Bollinger band {bbl:.2f}")
    reasons = [f"Above SMA200 {sma200:.2f} - long-term trend intact", rsi_txt, band_txt]
    quality = 45
    quality += 10 if rsi > rsi_prev else 0
    quality += 10 if k > d else 0
    quality += 10 if _num(s.get("open")) and c > s["open"] else 0
    quality += 5 if _num(s.get("ema20")) and (s["ema20"] - c) >= 1.5 * atr else 0  # room to mean
    stop = low - 0.75 * atr
    return {"setup": "BOUNCE", "stop_raw": stop, "quality": quality, "reasons": reasons}


SETUPS = (pullback, breakout, bounce)


# ───────────────────────────── trade plan ─────────────────────────────────

def plan_trade(s, hit, cfg, risk_mult=1.0):
    """Levels on the stock's tick grid plus share count.

    `warnings` are trade-quality concerns and lower the ranking; `notes` are
    sizing facts (e.g. a cap kicked in) and do not.
    """
    atr, tick = s["atr"], tick_size(s)
    high = s["high"] if _num(s.get("high")) else s["close"]
    entry = _to_tick(max(entry_raw(s), high + tick), tick, "up")   # strictly above today's high
    stop = _to_tick(hit["stop_raw"], tick, "down")
    r = entry - stop
    if r < tick / 2:
        return None
    t1, t2 = _to_tick(entry + 1.5 * r, tick, "near"), _to_tick(entry + 3.0 * r, tick, "near")
    if hit["setup"] == "BOUNCE" and _num(s.get("ema20")) and s["ema20"] > entry:
        # mean-reversion target: EMA20, kept between 1R and 1.5R
        t1 = _to_tick(min(max(s["ema20"], entry + r), entry + 1.5 * r), tick, "near")

    warnings, notes = [], []
    h1m, h52 = s.get("high_1m"), s.get("high_52w")
    if hit["setup"] != "BREAKOUT" and _num(h1m) and entry < h1m < t1:
        warnings.append(f"1M high {h1m:g} sits below T1 - resistance")
    elif _num(h52) and entry < h52 < t1:
        warnings.append(f"52W high {h52:g} sits below T1 - resistance")
    if _num(s.get("perf_1m")) and s["perf_1m"] > 25:
        warnings.append(f"Up {s['perf_1m']:.0f}% in 1M - extended")

    risk_budget = cfg["capital"] * cfg["risk_pct"] / 100 * risk_mult
    shares = int(risk_budget // r)
    caps = {"position": int(cfg["capital"] * cfg["max_position_pct"] / 100 // entry)}
    if _num(s.get("adv_egp")):
        caps["liquidity"] = int(s["adv_egp"] * cfg["max_adv_pct"] / 100 // entry)
    which = min(caps, key=caps.get)
    if caps[which] < shares:
        shares = caps[which]
        notes.append(f"Size capped by {which} limit")
    shares = max(shares, 0)
    dp = _decimals(tick)

    return {
        "entry": entry, "stop": stop, "t1": t1, "t2": t2, "tick": tick, "decimals": dp,
        "risk_per_share": round(r, dp),
        "risk_pct_of_price": round(r / entry * 100, 1),
        "rr_t1": round((t1 - entry) / r, 2),
        "shares": shares,
        "position_egp": round(shares * entry),
        "risk_egp": round(shares * r),
        "warnings": warnings, "notes": notes,
    }


# ───────────────────────────── scan ───────────────────────────────────────

def screen(stock, cfg):
    """Return (reason excluded or None, derived fields). Does not modify `stock`."""
    c, atr, vavg = stock.get("close"), stock.get("atr"), stock.get("vol_avg_10d")
    cur = stock.get("currency")
    if cur and cur != "EGP":
        return f"quoted in {cur} - EGP-only sizing", {}
    if not _num(c, atr, vavg) or c <= 0:
        return "missing data", {}
    derived = {"adv_egp": c * vavg, "atr_pct": atr / c * 100}
    if derived["adv_egp"] < cfg["min_adv_egp"]:
        return (f"ADV {derived['adv_egp'] / 1e6:.1f}M EGP < {cfg['min_adv_egp'] / 1e6:.1f}M"), derived
    if not cfg["min_atr_pct"] <= derived["atr_pct"] <= cfg["max_atr_pct"]:
        return (f"ATR {derived['atr_pct']:.1f}% outside "
                f"{cfg['min_atr_pct']}-{cfg['max_atr_pct']}%"), derived
    return None, derived


def scan(stocks, index, cfg=None):
    cfg = {**DEFAULTS, **(cfg or {})}
    regime = market_regime(index)
    idx_perf = index.get("perf_1m")
    signals, excluded = [], []

    for raw in stocks:
        why, derived = screen(raw, cfg)
        if why:
            excluded.append({"symbol": raw.get("symbol"), "reason": why})
            continue
        s = {**raw, **derived}
        for detect in SETUPS:
            hit = detect(s)
            if not hit:
                continue
            if hit["setup"] == "BREAKOUT" and regime["regime"] in ("RISK-OFF", "UNKNOWN"):
                continue
            plan = plan_trade(s, hit, cfg, regime["risk_mult"])
            if not plan or plan["shares"] == 0:
                continue
            quality = hit["quality"]
            rs = None
            if _num(s.get("perf_1m"), idx_perf):
                rs = round(s["perf_1m"] - idx_perf, 1)
                quality += 10 if rs > 3 else (-10 if rs < -3 else 0)
            quality -= 5 * len(plan["warnings"])
            signals.append({
                "symbol": s["symbol"], "name": s.get("name"), "sector": s.get("sector"),
                "setup": hit["setup"], "quality": quality, "reasons": hit["reasons"],
                "close": s["close"], "atr": s["atr"], "atr_pct": round(s["atr_pct"], 1),
                "adv_egp": round(s["adv_egp"]),
                "ema10": s.get("ema10") if _num(s.get("ema10")) else None,
                "rsi": round(s["rsi"], 1) if _num(s.get("rsi")) else None,
                "rs_vs_egx30": rs, **plan,
            })
            break   # one setup per stock: first match wins (PULLBACK > BREAKOUT > BOUNCE)

    signals.sort(key=lambda x: x["quality"], reverse=True)
    return {"regime": regime, "config": cfg, "signals": signals,
            "excluded": excluded, "scanned": len(stocks)}
