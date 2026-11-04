"""Replay the scanner's exact rules over daily history and simulate the trades.

The setups, regime filter, tick rounding and position sizing come straight from
egx_swing.setups, so the backtest tests the same logic that writes the emails.
Indicators use egx_swing.indicators (TradingView definitions), computed once per
stock as full series instead of once per day.

Trade rules (same as the emails):
- signal on the close of day D -> buy-stop at the plan's entry, valid for the next
  `valid_days` sessions; fill at max(entry, open) when the day's high reaches it
- after a fill: stop-loss; at T1 sell half and move the stop to the fill price; T2 sells the rest
- exit at the close after `max_hold` sessions if still open
- a day whose range touches both the stop and a target counts as the stop (conservative)
- Thndr fees on every buy and sell (backtest/fees.py)
"""

from bisect import bisect_left
from datetime import date, timedelta

from egx_swing import indicators as ind
from egx_swing import setups

from .fees import order_fees

FEES = {
    "brokerage_fixed": 2.0, "brokerage_pct": 0.001, "commission_waived": False,
    "egx_pct": 0.0001, "egx_max": 5000.0, "mcdr_pct": 0.0001, "mcdr_max": 5000.0,
    "fra_pct": 0.00005, "fra_min": 1.0, "fra_max": 250.0,
    "insurance_pct": 0.00005, "insurance_max": 5000.0,
    "stamp_pct": 0.0005, "stamp_pct_t0": 0.00025,
}


# ───────────────────────── indicator series ─────────────────────────

def daily_rows(symbol, candles):
    """Per-day dicts with the screener fields setups.scan() reads. Oldest first.
    Days with fewer than MIN_BARS of history are left out."""
    n = len(candles)
    if n < ind.MIN_BARS:
        return {}
    o = [c["open"] for c in candles]
    h = [c["high"] for c in candles]
    lo = [c["low"] for c in candles]
    c = [c_["close"] for c_ in candles]
    v = [c_["volume"] or 0 for c_ in candles]
    dates = [date.fromisoformat(x["date"]) if isinstance(x["date"], str) else x["date"] for x in candles]

    ema10, ema20, ema50 = ind.ema(c, 10), ind.ema(c, 20), ind.ema(c, 50)
    sma200, basis = ind.sma(c, 200), ind.sma(c, 20)
    ema12, ema26 = ind.ema(c, 12), ind.ema(c, 26)
    macd = [a - b if a is not None and b is not None else None for a, b in zip(ema12, ema26)]
    macd_sig = ind.ema(macd, 9)
    rsi = ind.rsi(c)
    k, d = ind.stoch(h, lo, c)
    adx, dip, dim = ind.adx(h, lo, c)
    atr = ind.rma(ind.true_range(h, lo, c), 14)

    out = {}
    for i in range(ind.MIN_BARS - 1, n):
        day = dates[i]
        if None in (ema50[i], sma200[i], atr[i], rsi[i], k[i], d[i]):
            continue
        win = c[i - 19:i + 1]
        sd = (sum((x - basis[i]) ** 2 for x in win) / 20) ** 0.5
        m_ago = ind._months_back(day, 1)
        j = bisect_left(dates, m_ago, 0, i + 1)          # first index with date >= month_ago
        ref = c[j - 1] if j > 0 else None
        y_ago = day - timedelta(days=365)
        jy = bisect_left(dates, y_ago + timedelta(days=1), 0, i + 1)
        jm = bisect_left(dates, m_ago + timedelta(days=1), 0, i + 1)
        out[day] = {
            "symbol": symbol, "currency": "EGP", "bar_date": day.isoformat(),
            "open": o[i], "high": h[i], "low": lo[i], "close": c[i],
            "ema10": ema10[i], "ema20": ema20[i], "ema50": ema50[i], "sma200": sma200[i],
            "rsi": rsi[i], "rsi_prev": rsi[i - 1],
            "macd": macd[i], "macd_signal": macd_sig[i],
            "stoch_k": k[i], "stoch_d": d[i], "stoch_k_prev": k[i - 1], "stoch_d_prev": d[i - 1],
            "bb_lower": basis[i] - 2 * sd,
            "adx": adx[i], "di_plus": dip[i], "di_minus": dim[i], "atr": atr[i],
            "perf_1m": (c[i] / ref - 1) * 100 if ref else None,
            "high_1m": max(h[jm:i + 1]), "high_52w": max(h[jy:i + 1]),
            "volume": v[i], "vol_avg_10d": sum(v[i - 9:i + 1]) / 10,
        }
    return out


def index_rows(candles):
    """EGX30 per day: close, ema20, ema50, perf_1m (what market_regime() needs)."""
    c = [x["close"] for x in candles]
    dates = [date.fromisoformat(x["date"]) for x in candles]
    e20, e50 = ind.ema(c, 20), ind.ema(c, 50)
    out = {}
    for i, day in enumerate(dates):
        if e50[i] is None:
            continue
        m_ago = ind._months_back(day, 1)
        j = bisect_left(dates, m_ago, 0, i + 1)
        out[day] = {"close": c[i], "ema20": e20[i], "ema50": e50[i],
                    "perf_1m": (c[i] / c[j - 1] - 1) * 100 if j > 0 else None}
    return out


# ───────────────────────── signal generation ─────────────────────────

def generate_signals(stock_rows, idx_rows, cfg):
    """Run setups.scan() for every session. Returns {day: (regime, [signals])}."""
    days = sorted(idx_rows)
    out = {}
    for day in days:
        stocks = [rows[day] for rows in stock_rows.values() if day in rows]
        if not stocks:
            continue
        res = setups.scan(stocks, idx_rows[day], cfg)
        out[day] = (res["regime"]["regime"], res["signals"])
    return out


def donchian_signals(stock_rows, idx_rows, cfg, n=50, stop_atr=2.0):
    """Trend entry: close at a new n-session high, above SMA200 and EMA50 > SMA200.
    Same liquidity/volatility screen and sizing as the scanner; entry is a buy-stop
    one tick-ish above today's high, stop = entry - stop_atr * ATR."""
    cfg = {**setups.DEFAULTS, **cfg}
    hist = {}
    for sym, rows in stock_rows.items():
        days = sorted(rows)
        highs = [rows[d]["high"] for d in days]
        for i in range(n, len(days)):
            s = rows[days[i]]
            if s["close"] >= max(highs[i - n:i]) and s["close"] > s["sma200"] and s["ema50"] > s["sma200"]:
                hist.setdefault(days[i], []).append(s)
    out = {}
    for day in sorted(idx_rows):
        regime = setups.market_regime(idx_rows[day])
        sigs = []
        for s in hist.get(day, []):
            why, derived = setups.screen(s, cfg)
            if why:
                continue
            s2 = {**s, **derived}
            tick = setups.tick_size(s2)
            entry = setups._to_tick(s2["high"] + 0.1 * s2["atr"], tick, "up")
            stop = setups._to_tick(entry - stop_atr * s2["atr"], tick, "down")
            r = entry - stop
            if r <= 0:
                continue
            risk = cfg["capital"] * cfg["risk_pct"] / 100 * regime["risk_mult"]
            shares = min(int(risk // r), int(cfg["capital"] * cfg["max_position_pct"] / 100 // entry),
                         int(derived["adv_egp"] * cfg["max_adv_pct"] / 100 // entry))
            if shares <= 0:
                continue
            idx_perf = idx_rows[day].get("perf_1m")
            rs = (s2["perf_1m"] - idx_perf) if s2.get("perf_1m") is not None and idx_perf is not None else 0
            sigs.append({"symbol": s2["symbol"], "setup": "DONCHIAN", "quality": round(50 + rs),
                         "entry": entry, "stop": stop, "shares": shares})
        sigs.sort(key=lambda x: x["quality"], reverse=True)
        out[day] = (regime["regime"], sigs)
    return out


# ───────────────────────── trade simulation ─────────────────────────

def _fees(value):
    return order_fees(value, FEES)["total"]


def simulate(signals_by_day, bars_by_symbol, variant):
    """Portfolio simulation of one variant. Returns (trades, equity_curve).

    variant keys:
      capital, gate ("as_is" | "no_buy_riskoff" | "no_buy_unless_riskon"),
      t1_r, t2_r (target multiples of entry-stop risk), max_hold, valid_days,
      top_n (max new orders per day), max_positions, min_quality
    """
    cap = variant["capital"]
    cash, positions, pending, trades, curve = cap, {}, [], [], []
    first = min(signals_by_day) if signals_by_day else None
    days = sorted({d for bars in bars_by_symbol.values() for d in bars if first is None or d >= first})
    day_ix = {d: i for i, d in enumerate(days)}

    for day in days:
        # 1) manage open positions on today's bar
        for sym in list(positions):
            p = positions[sym]
            bar = bars_by_symbol[sym].get(day)
            if not bar:
                continue
            o, h, l, c = bar
            p["held"] += 1
            exits = []
            stop = p["stop"]
            if variant.get("exit") == "trail":
                # trend mode: no fixed targets; a stop that only moves up, plus an optional moving-average exit
                row = variant["_aux"].get(sym, {}).get(day)
                if l <= stop:
                    exits.append(("STOP" if stop <= p["stop0"] else "TRAIL", min(o, stop), p["qty"]))
                else:
                    p["hh"] = max(p.get("hh", p["fill"]), h)
                    if row:
                        k = variant.get("trail_atr")
                        if k:
                            p["stop"] = max(p["stop"], p["hh"] - k * row["atr"])
                        ma = variant.get("trail_ma")
                        if ma and c < row[ma]:
                            exits.append((f"BELOW_{ma.upper()}", c, p["qty"]))
            elif l <= stop and not (p["fill_day"] == day and p["half"]):
                px = min(o, stop) if p["fill_day"] != day else stop
                exits.append(("STOP" if not p["half"] else "BREAKEVEN", px, p["qty"]))
            if variant.get("exit") == "trail":
                pass
            elif exits:
                pass
            else:
                if not p["half"] and h >= p["t1"]:
                    half = p["qty"] // 2
                    px = max(o, p["t1"]) if p["fill_day"] != day else p["t1"]
                    if half:
                        exits.append(("T1", px, half))
                    p["half"] = True
                    p["stop"] = p["fill"]
                if p["half"] and h >= p["t2"] and p["fill_day"] != day:
                    exits.append(("T2", max(o, p["t2"]), p["qty"] - sum(q for _, _, q in exits)))
            sold = sum(q for _, _, q in exits)
            if not exits and p["held"] >= variant["max_hold"]:
                exits.append(("TIME", c, p["qty"])); sold = p["qty"]
            elif exits and sold < p["qty"] and p["held"] >= variant["max_hold"]:
                exits.append(("TIME", c, p["qty"] - sold)); sold = p["qty"]
            for why, px, q in exits:
                if q <= 0:
                    continue
                val = q * px
                fee = _fees(val)
                cash += val - fee
                p["proceeds"] += val - fee
                p["exits"].append((day.isoformat(), why, round(px, 3), q))
            p["qty"] -= sold
            if p["qty"] <= 0:
                pnl = p["proceeds"] - p["cost"]
                trades.append({**{k: p[k] for k in ("symbol", "setup", "quality", "regime", "signal_day",
                                                      "entry", "stop0", "t1", "t2", "fill", "shares")},
                               "fill_day": p["fill_day"].isoformat(), "exit_day": day.isoformat(),
                               "exits": p["exits"], "days_held": p["held"],
                               "pnl_egp": round(pnl, 2), "risk_egp": round(p["risk_egp"], 2),
                               "r": round(pnl / p["risk_egp"], 3) if p["risk_egp"] else 0,
                               "outcome": p["exits"][-1][1] if len(p["exits"]) == 1 else
                                          "+".join(e[1] for e in p["exits"])})
                del positions[sym]

        # 2) fill pending buy-stops
        still = []
        for o_ in pending:
            sym = o_["symbol"]
            bar = bars_by_symbol[sym].get(day)
            if day_ix[day] > o_["expires_ix"]:
                continue
            if not bar:
                still.append(o_); continue
            op, h, l, c = bar
            if h < o_["entry"]:
                still.append(o_); continue
            if sym in positions or len(positions) >= variant["max_positions"]:
                continue
            fill = max(op, o_["entry"])
            r = fill - o_["stop"]
            if r <= 0:
                continue
            qty = o_["shares"]
            cost = qty * fill + _fees(qty * fill)
            if cost > cash or qty <= 0:
                continue            # not enough free cash: skip, as a real account would
            cash -= cost
            positions[sym] = {**o_, "fill": fill, "fill_day": day, "qty": qty, "shares": qty,
                              "half": False, "held": 0, "cost": cost, "proceeds": 0.0,
                              "risk_egp": qty * r, "exits": [], "stop0": o_["stop"]}
            # same-day stop check for the fill bar is handled in the next loop pass:
            p = positions[sym]
            if l <= p["stop"]:
                val = qty * p["stop"]; fee = _fees(val); cash += val - fee
                trades.append({**{k: p[k] for k in ("symbol", "setup", "quality", "regime", "signal_day",
                                                      "entry", "stop0", "t1", "t2", "fill", "shares")},
                               "fill_day": day.isoformat(), "exit_day": day.isoformat(),
                               "exits": [(day.isoformat(), "STOP", p["stop"], qty)], "days_held": 0,
                               "pnl_egp": round(val - fee - cost, 2), "risk_egp": round(p["risk_egp"], 2),
                               "r": round((val - fee - cost) / p["risk_egp"], 3), "outcome": "STOP"})
                del positions[sym]
        pending = still

        # 3) new signals from today's close
        regime, sigs = signals_by_day.get(day, (None, []))
        gate = variant["gate"]
        allow = not ((gate == "no_buy_riskoff" and regime in ("RISK-OFF", "UNKNOWN")) or
                     (gate == "no_buy_unless_riskon" and regime != "RISK-ON"))
        if allow:
            taken = 0
            for s in sigs:
                if s["quality"] < variant["min_quality"] or s["symbol"] in positions:
                    continue
                if any(p_["symbol"] == s["symbol"] for p_ in pending):
                    continue
                r = s["entry"] - s["stop"]
                pending.append({"symbol": s["symbol"], "setup": s["setup"], "quality": s["quality"],
                                "regime": regime, "signal_day": day.isoformat(),
                                "entry": s["entry"], "stop": s["stop"],
                                "t1": s["entry"] + variant["t1_r"] * r, "t2": s["entry"] + variant["t2_r"] * r,
                                "shares": s["shares"], "expires_ix": day_ix[day] + variant["valid_days"]})
                taken += 1
                if taken >= variant["top_n"]:
                    break

        # 4) mark to market
        mtm = sum(p["qty"] * bars_by_symbol[s_][day][3] for s_, p in positions.items()
                  if day in bars_by_symbol[s_]) + \
              sum(p["qty"] * p["fill"] for s_, p in positions.items() if day not in bars_by_symbol[s_])
        curve.append((day.isoformat(), round(cash + mtm, 2), len(positions)))
    return trades, curve


def metrics(trades, curve, capital):
    if not trades:
        return {"trades": 0}
    rs = [t["r"] for t in trades]
    wins = [r for r in rs if r > 0]
    peak, dd = capital, 0.0
    for _, eq, _ in curve:
        peak = max(peak, eq)
        dd = min(dd, eq / peak - 1)
    final = curve[-1][1]
    years = max((date.fromisoformat(curve[-1][0]) - date.fromisoformat(curve[0][0])).days / 365.25, 0.01)
    gross_win = sum(t["pnl_egp"] for t in trades if t["pnl_egp"] > 0)
    gross_loss = -sum(t["pnl_egp"] for t in trades if t["pnl_egp"] < 0)
    by_outcome = {}
    for t in trades:
        by_outcome[t["outcome"]] = by_outcome.get(t["outcome"], 0) + 1
    return {
        "trades": len(trades),
        "win_rate_pct": round(100 * len(wins) / len(trades), 1),
        "avg_r": round(sum(rs) / len(rs), 3),
        "profit_factor": round(gross_win / gross_loss, 2) if gross_loss else None,
        "total_return_pct": round((final / capital - 1) * 100, 1),
        "cagr_pct": round(((final / capital) ** (1 / years) - 1) * 100, 1) if final > 0 else None,
        "max_drawdown_pct": round(dd * 100, 1),
        "avg_days_held": round(sum(t["days_held"] for t in trades) / len(trades), 1),
        "fees_note": "all results are after Thndr fees",
        "outcomes": by_outcome,
    }
