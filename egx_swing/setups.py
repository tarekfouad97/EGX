"""Swing setup detection and trade planning.

Three long-only setups, each evaluated on the latest daily bar:

  PULLBACK  - established uptrend, price has dipped back to the 20 EMA and
              momentum is turning up again.
  BREAKOUT  - close at/through the 1-month high on expanding volume with a
              trending ADX.
  BOUNCE    - oversold reversal while the long-term (200 SMA) trend is intact.

Every candidate gets a buy-stop entry above today's high, an ATR-based stop,
two R-multiple targets, and a quality score used for ranking. All functions
are pure: they take dicts of indicator values and return dicts.
"""

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
    return all(isinstance(v, (int, float)) for v in vals)


def _tick(price):
    """Round to the 0.01 EGP tick."""
    return round(price + 1e-9, 2)


# ───────────────────────────── market regime ──────────────────────────────

def market_regime(index):
    """RISK-ON / NEUTRAL / RISK-OFF from EGX30 vs its moving averages."""
    close, ema20, ema50 = index.get("close"), index.get("ema20"), index.get("ema50")
    if not _num(close, ema20, ema50):
        return {"regime": "UNKNOWN", "risk_mult": 0.5,
                "note": "EGX30 data unavailable - risk halved"}
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
    turning = k > d and k < 60
    if not (uptrend and near_ema and reset and turning):
        return None
    reasons = [f"Uptrend: EMA20 {e20:.2f} > EMA50 {e50:.2f} > SMA200 {sma200:.2f}",
               f"Dipped to EMA20 (low {low:.2f})",
               f"RSI {rsi:.0f} reset, Stoch %K {k:.0f} crossing above %D {d:.0f}"]
    quality = 50
    quality += 10 if s.get("adx") and s["adx"] > 20 else 0
    quality += 10 if _num(s.get("macd"), s.get("macd_signal")) and s["macd"] > s["macd_signal"] else 0
    quality += 10 if 42 <= rsi <= 52 else 0
    quality += 10 if c > s.get("open", c) else 0          # bullish candle
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
    stop = c - 1.5 * atr
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
    reasons = [f"Above SMA200 {sma200:.2f} - long-term trend intact",
               f"RSI {rsi:.0f} (prev {rsi_prev:.0f}) oversold and turning",
               f"Tagged lower Bollinger band {bbl:.2f}"]
    quality = 45
    quality += 10 if rsi > rsi_prev else 0
    quality += 10 if k > d else 0
    quality += 10 if c > s.get("open", c) else 0
    quality += 5 if _num(s.get("ema20")) and (s["ema20"] - c) >= 1.5 * atr else 0  # room to mean
    stop = low - 0.75 * atr
    return {"setup": "BOUNCE", "stop_raw": stop, "quality": quality, "reasons": reasons}


SETUPS = (pullback, breakout, bounce)


# ───────────────────────────── trade plan ─────────────────────────────────

def plan_trade(s, hit, cfg, risk_mult=1.0):
    atr, high = s["atr"], s.get("high") or s["close"]
    entry = _tick(high + 0.1 * atr)          # buy-stop just above today's high
    stop = _tick(hit["stop_raw"])
    r = entry - stop
    if r <= 0:
        return None
    t1, t2 = _tick(entry + 1.5 * r), _tick(entry + 3.0 * r)
    if hit["setup"] == "BOUNCE" and _num(s.get("ema20")) and s["ema20"] > entry:
        t1 = _tick(max(min(s["ema20"], t1), entry + r))   # mean-reversion target

    warnings = []
    h1m = s.get("high_1m")
    if hit["setup"] != "BREAKOUT" and _num(h1m) and entry < h1m < t1:
        warnings.append(f"1M high {h1m:.2f} sits below T1 - resistance")
    if _num(s.get("high_52w")) and entry < s["high_52w"] < t1 and s["high_52w"] != h1m:
        warnings.append(f"52W high {s['high_52w']:.2f} sits below T1")
    if _num(s.get("perf_1m")) and s["perf_1m"] > 25:
        warnings.append(f"Up {s['perf_1m']:.0f}% in 1M - extended")

    risk_egp = cfg["capital"] * cfg["risk_pct"] / 100 * risk_mult
    shares = int(risk_egp // r)
    caps = [int(cfg["capital"] * cfg["max_position_pct"] / 100 // entry)]
    adv = s.get("adv_egp")
    if adv:
        caps.append(int(adv * cfg["max_adv_pct"] / 100 // entry))
    capped = min(caps)
    if capped < shares:
        shares = capped
        warnings.append("Size capped by position/liquidity limit")

    return {
        "entry": entry, "stop": stop, "t1": t1, "t2": t2,
        "risk_per_share": round(r, 2),
        "risk_pct_of_price": round(r / entry * 100, 1),
        "rr_t1": round((t1 - entry) / r, 2),
        "shares": max(shares, 0),
        "position_egp": round(max(shares, 0) * entry),
        "risk_egp": round(max(shares, 0) * r),
        "warnings": warnings,
    }


# ───────────────────────────── scan ───────────────────────────────────────

def screen(stock, cfg):
    """Return the reason a stock is excluded, or None if it is tradeable."""
    c, atr, vavg = stock.get("close"), stock.get("atr"), stock.get("vol_avg_10d")
    if not _num(c, atr, vavg) or c <= 0:
        return "missing data"
    adv = c * vavg
    stock["adv_egp"] = adv
    stock["atr_pct"] = atr / c * 100
    if adv < cfg["min_adv_egp"]:
        return f"ADV {adv / 1e6:.1f}M EGP < {cfg['min_adv_egp'] / 1e6:.0f}M"
    if not cfg["min_atr_pct"] <= stock["atr_pct"] <= cfg["max_atr_pct"]:
        return f"ATR {stock['atr_pct']:.1f}% outside {cfg['min_atr_pct']}-{cfg['max_atr_pct']}%"
    return None


def scan(stocks, index, cfg=None):
    cfg = {**DEFAULTS, **(cfg or {})}
    regime = market_regime(index)
    idx_perf = index.get("perf_1m")
    signals, excluded = [], []

    for s in stocks:
        why = screen(s, cfg)
        if why:
            excluded.append({"symbol": s.get("symbol"), "reason": why})
            continue
        for detect in SETUPS:
            hit = detect(s)
            if not hit:
                continue
            if hit["setup"] == "BREAKOUT" and regime["regime"] == "RISK-OFF":
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
                "close": s["close"], "atr": round(s["atr"], 2),
                "atr_pct": round(s["atr_pct"], 1), "adv_egp": round(s["adv_egp"]),
                "rsi": round(s["rsi"], 1) if _num(s.get("rsi")) else None,
                "rs_vs_egx30": rs, **plan,
            })
            break   # one setup per stock: first match wins (PULLBACK > BREAKOUT > BOUNCE)

    signals.sort(key=lambda x: x["quality"], reverse=True)
    return {"regime": regime, "config": cfg, "signals": signals,
            "excluded": excluded, "scanned": len(stocks)}
