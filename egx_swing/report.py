"""Markdown rendering of a scan result."""


def _m(x):
    return f"{x / 1e6:,.1f}M"


def render(result, index, when):
    reg = result["regime"]
    cfg = result["config"]
    sig = result["signals"]
    out = [f"# EGX Swing Scan - {when}", ""]

    idx = ""
    if index.get("close") is not None:
        idx = f" | EGX30 {index['close']:,.0f}"
        if index.get("perf_1m") is not None:
            idx += f" ({index['perf_1m']:+.1f}% 1M)"
    out += [f"**Regime: {reg['regime']}**{idx} - {reg['note']}", ""]
    out += [f"Scanned {result['scanned']} stocks, {len(result['excluded'])} filtered out "
            f"(liquidity/volatility), **{len(sig)} setups**. "
            f"Sizing: {cfg['capital']:,.0f} EGP capital, {cfg['risk_pct']}% risk/trade "
            f"x {reg['risk_mult']} regime multiplier.", ""]

    if not sig:
        out += ["_No setups today. Cash is a position._", ""]
    else:
        out += ["| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | Risk % | Shares | Position EGP |",
                "|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------------|"]
        for i, s in enumerate(sig, 1):
            out.append(f"| {i} | **{s['symbol']}** | {s['setup']} | {s['quality']} | {s['close']:.2f} | "
                       f"{s['entry']:.2f} | {s['stop']:.2f} | {s['t1']:.2f} | {s['t2']:.2f} | "
                       f"{s['risk_pct_of_price']}% | {s['shares']:,} | {s['position_egp']:,} |")
        out.append("")
        for i, s in enumerate(sig, 1):
            rs = f" | RS vs EGX30 {s['rs_vs_egx30']:+.1f}pts" if s["rs_vs_egx30"] is not None else ""
            out += [f"### {i}. {s['symbol']} - {s['name']} ({s['setup']})",
                    f"{s['sector']} | ATR {s['atr']} ({s['atr_pct']}%/day) | ADV {_m(s['adv_egp'])} EGP"
                    f" | RSI {s['rsi']}{rs}", ""]
            out += [f"- {r}" for r in s["reasons"]]
            out += [f"- ⚠ {w}" for w in s["warnings"]]
            out.append("")

    out += ["## How to use",
            "- **Entry** is a buy-stop above today's high: only trigger if price trades through it "
            "next session. Cancel if not filled within 2 sessions.",
            "- **Stop** is hard. Sell half at **T1** (1.5R), move stop to entry, trail the rest to **T2** (3R) "
            "or exit on a close below EMA10.",
            "- Time stop: exit after ~10 sessions if neither target nor stop is hit.",
            "", "_Analytical output only - not licensed financial advice._", ""]
    return "\n".join(out)
