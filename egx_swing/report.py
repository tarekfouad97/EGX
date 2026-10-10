"""Markdown rendering of a scan result."""


def _m(x):
    return f"{x / 1e6:,.1f}M"


def render(result, index, when):
    reg = result["regime"]
    cfg = result["config"]
    sig = result["signals"]
    status = result.get("run_status", "OK")
    out = [f"# EGX Swing Scan - session {result.get('as_of') or 'unknown'}", "",
           f"_Generated {when}. Run status: **{status}**._", ""]
    if status == "FAILED":
        out += ["> ⛔ No usable market data this run - **no trades**. See Data quality below.", ""]
    elif status == "DEGRADED":
        out += ["> ⚠ Some data came from the fallback source or was dropped. See Data quality below.", ""]
    if result.get("intraday"):
        out += ["> ⚠ EGX session may still be open - this bar is not final.", ""]

    idx = ""
    if index.get("close") is not None:
        idx = f" | EGX30 {index['close']:,.0f}"
        if index.get("perf_1m") is not None:
            idx += f" ({index['perf_1m']:+.1f}% 1M)"
    out += [f"**Regime: {reg['regime']}**{idx} - {reg['note']}", ""]
    out += [f"Scanned {result['scanned']} stocks, {len(result['excluded'])} filtered out "
            f"(currency/liquidity/volatility), **{len(sig)} setups**. "
            f"Sizing: {cfg['capital']:,.0f} EGP capital, {cfg['risk_pct']}% risk/trade "
            f"x {reg['risk_mult']} regime multiplier.", ""]

    if not sig:
        out += ["_No setups today. Cash is a position._", ""]
    else:
        out += ["| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |",
                "|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|"]
        for i, s in enumerate(sig, 1):
            d = s["decimals"]
            out.append(f"| {i} | **{s['symbol']}** | {s['setup']} | {s['quality']} | {s['close']:.{d}f} | "
                       f"{s['entry']:.{d}f} | {s['stop']:.{d}f} | {s['t1']:.{d}f} | {s['t2']:.{d}f} | "
                       f"{s['rr_t1']:.1f}R | {s['risk_pct_of_price']}% | {s['shares']:,} | {s['position_egp']:,} |")
        out.append("")
        for i, s in enumerate(sig, 1):
            d = s["decimals"] + 1
            rs = f" | RS vs EGX30 {s['rs_vs_egx30']:+.1f}pts" if s["rs_vs_egx30"] is not None else ""
            ema10 = f" | EMA10 {s['ema10']:.{d}f}" if s.get("ema10") is not None else ""
            out += [f"### {i}. {s['symbol']} - {s['name']} ({s['setup']})",
                    f"{s['sector']} | ATR {s['atr']:.{d}f} ({s['atr_pct']}%/day) | ADV {_m(s['adv_egp'])} EGP"
                    f" | RSI {s['rsi']}{ema10}{rs}", ""]
            out += [f"- {r}" for r in s["reasons"]]
            out += [f"- ⚠ {w}" for w in s["warnings"]]
            out += [f"- ℹ {n}" for n in s.get("notes", [])]
            out.append("")

    out += _data_quality(result)
    out += ["## How to use",
            "- **Entry** is a buy-stop above the session's high: only trigger if price trades through it "
            "in the next session. Cancel if not filled within 2 sessions.",
            "- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, "
            "trail the rest to **T2** (3R) or exit on a close below EMA10.",
            "- Time stop: exit after ~10 sessions if neither target nor stop is hit.",
            "", "_Analytical output only - not licensed financial advice._", ""]
    return "\n".join(out)


def _data_quality(result):
    status = result.get("data_status") or {}
    events = result.get("events") or []
    if not status and not events:
        return []
    by = {}
    for sym, st in sorted(status.items()):
        by.setdefault(st["state"], []).append((sym, st.get("reason", "")))
    out = ["## Data quality", "",
           f"Universe {result.get('universe', 0)} | screener OK {len(by.get('READY', []))} | "
           f"recovered from fallback {len(by.get('RECOVERED', []))} | dropped {len(by.get('DROPPED', []))}", ""]
    if by.get("RECOVERED"):
        out += ["**Recovered** (indicators computed from Yahoo daily candles):", ""]
        out += [f"- {sym}: {why}" for sym, why in by["RECOVERED"]]
        out.append("")
    if by.get("DROPPED"):
        out += ["**Dropped** (no fresh, complete data from any source):", ""]
        out += [f"- {sym}: {why}" for sym, why in by["DROPPED"]]
        out.append("")
    if events:
        out += ["<details><summary>Run log</summary>", "", "| Stage | Outcome | Detail |", "|---|---|---|"]
        out += [f"| {e['stage']} | {e['outcome']} | {e['detail'].replace('|', '/')} |" for e in events]
        out += ["", "</details>", ""]
    return out
