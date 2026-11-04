"""Backtest the scanner on cached history and compare strategy variants.

    python -m backtest.run --history data/history --out backtest/results

Writes summary.md, summary.json and one trades CSV per variant.
"""

import argparse
import csv
import json
from datetime import date
from pathlib import Path

from .engine import daily_rows, donchian_signals, generate_signals, index_rows, metrics, simulate

BASE = {"capital": 20000.0, "gate": "as_is", "t1_r": 1.5, "t2_r": 3.0, "max_hold": 10,
        "valid_days": 2, "top_n": 99, "max_positions": 99, "min_quality": -999}

VARIANTS = {
    "A_as_emailed":            {},
    "B_no_buys_in_riskoff":    {"gate": "no_buy_riskoff"},
    "C_riskon_only":           {"gate": "no_buy_unless_riskon"},
    "D_top5_q70":              {"gate": "no_buy_riskoff", "top_n": 5, "min_quality": 70, "max_positions": 8},
    "E_D_plus_t1_1R":          {"gate": "no_buy_riskoff", "top_n": 5, "min_quality": 70, "max_positions": 8,
                                "t1_r": 1.0, "t2_r": 2.0},
    "F_D_plus_t1_1.25R":       {"gate": "no_buy_riskoff", "top_n": 5, "min_quality": 70, "max_positions": 8,
                                "t1_r": 1.25, "t2_r": 2.5},
    "G_as_emailed_t1_1R":      {"t1_r": 1.0, "t2_r": 2.0},
}

# Trend-following: same scanner entries or a 50-day-high breakout, but no fixed targets.
TREND = {"exit": "trail", "max_hold": 250, "t1_r": 99, "t2_r": 99}
TREND_VARIANTS = {
    # scanner entries, ride the trend
    "H_scan_riskon_trail3ATR":     ("scan", {**TREND, "gate": "no_buy_unless_riskon", "trail_atr": 3.0}),
    "I_scan_riskon_belowEMA50":    ("scan", {**TREND, "gate": "no_buy_unless_riskon", "trail_ma": "ema50"}),
    "J_scan_noRiskoff_trail3ATR":  ("scan", {**TREND, "gate": "no_buy_riskoff", "trail_atr": 3.0}),
    # classic trend entry: new 50-day high
    "K_donch50_trail3ATR":         ("donchian", {**TREND, "trail_atr": 3.0}),
    "L_donch50_riskon_trail3ATR":  ("donchian", {**TREND, "gate": "no_buy_unless_riskon", "trail_atr": 3.0}),
    "M_donch50_belowEMA50":        ("donchian", {**TREND, "trail_ma": "ema50"}),
    "N_donch50_trail4ATR":         ("donchian", {**TREND, "trail_atr": 4.0}),
    "O_donch50_riskon_trail3ATR_max6": ("donchian", {**TREND, "gate": "no_buy_unless_riskon", "trail_atr": 3.0,
                                                     "max_positions": 6}),
    # the exact rule the daily scanner now runs (egx_swing.setups.trend via scan())
    "P_LIVE_scanner_trend":        ("live", {**TREND, "trail_atr": 3.0}),
}


def load(path):
    rows = list(csv.DictReader(open(path)))
    out = []
    for r in rows:
        try:
            out.append({"date": r["date"], "open": float(r["open"]), "high": float(r["high"]),
                        "low": float(r["low"]), "close": float(r["close"]),
                        "volume": float(r["volume"] or 0)})
        except (TypeError, ValueError):
            continue
    return out


def by_setup(trades):
    out = {}
    for t in trades:
        g = out.setdefault(t["setup"], [])
        g.append(t["r"])
    return {k: {"trades": len(v), "avg_r": round(sum(v) / len(v), 3),
                "win_rate_pct": round(100 * sum(r > 0 for r in v) / len(v), 1)} for k, v in out.items()}


def by_regime(trades):
    out = {}
    for t in trades:
        out.setdefault(t["regime"], []).append(t["r"])
    return {k: {"trades": len(v), "avg_r": round(sum(v) / len(v), 3)} for k, v in out.items()}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", default="data/history")
    ap.add_argument("--out", default="backtest/results")
    ap.add_argument("--start", help="first signal date (YYYY-MM-DD) to include")
    a = ap.parse_args(argv)

    hist = Path(a.history)
    idx = load(hist / "EGX30.csv")
    stock_rows, bars = {}, {}
    for p in sorted(hist.glob("*.csv")):
        sym = p.stem
        if sym == "EGX30":
            continue
        c = load(p)
        rows = daily_rows(sym, c)
        if rows:
            stock_rows[sym] = rows
            bars[sym] = {date.fromisoformat(x["date"]): (x["open"], x["high"], x["low"], x["close"]) for x in c}
    print(f"{len(stock_rows)} stocks with enough history", flush=True)

    irows = index_rows(idx)
    cfg = {"capital": BASE["capital"], "risk_pct": 1.0}
    sigs = generate_signals(stock_rows, irows, cfg)
    dsigs = donchian_signals(stock_rows, irows, cfg)
    tsigs = generate_signals(stock_rows, irows, cfg, strategy="trend")   # the live scanner's trend rule
    if a.start:
        start = date.fromisoformat(a.start)
        sigs = {d: v for d, v in sigs.items() if d >= start}
        bars = {s: {d: b for d, b in bb.items() if d >= start} for s, bb in bars.items()}
    first0 = min(sigs)
    dsigs = {d: v for d, v in dsigs.items() if d >= first0}
    tsigs = {d: v for d, v in tsigs.items() if d >= first0}
    first, last = min(sigs), max(sigs)
    n_sig = sum(len(v[1]) for v in sigs.values())
    regimes = {}
    for reg, _ in sigs.values():
        regimes[reg] = regimes.get(reg, 0) + 1
    print(f"signals {n_sig} over {len(sigs)} sessions {first}..{last}; regimes {regimes}", flush=True)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    summary = {"period": [first.isoformat(), last.isoformat()], "sessions": len(sigs),
               "stocks": len(stock_rows), "raw_signals": n_sig, "regime_days": regimes, "variants": {}}
    runs = [(n, "scan", o) for n, o in VARIANTS.items()] + [(n, src, o) for n, (src, o) in TREND_VARIANTS.items()]
    for name, src, over in runs:
        v = {**BASE, **over, "_aux": stock_rows}
        trades, curve = simulate({"scan": sigs, "donchian": dsigs, "live": tsigs}[src], bars, v)
        v.pop("_aux")
        m = metrics(trades, curve, v["capital"])
        m["by_setup"] = by_setup(trades)
        m["by_regime"] = by_regime(trades)
        m["settings"] = v
        summary["variants"][name] = m
        with open(out / f"trades_{name}.csv", "w", newline="") as f:
            if trades:
                w = csv.DictWriter(f, fieldnames=list(trades[0].keys()))
                w.writeheader()
                w.writerows(trades)
        with open(out / f"equity_{name}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "equity", "open_positions"])
            w.writerows(curve)
        print(name, json.dumps({k: m.get(k) for k in ("trades", "win_rate_pct", "avg_r", "total_return_pct",
                                                      "max_drawdown_pct")}), flush=True)

    json.dump(summary, open(out / "summary.json", "w"), indent=1, default=str)
    lines = [f"# Backtest {first} to {last}", "",
             f"{len(stock_rows)} stocks, {len(sigs)} sessions, {n_sig} raw signals. Regime days: {regimes}.",
             "All results after Thndr fees, 20,000 EGP account.", "",
             "| Variant | Trades | Win % | Avg R | Profit factor | Return % | Max DD % | Avg days |",
             "|---|---|---|---|---|---|---|---|"]
    for name, m in summary["variants"].items():
        lines.append(f"| {name} | {m.get('trades')} | {m.get('win_rate_pct')} | {m.get('avg_r')} | "
                     f"{m.get('profit_factor')} | {m.get('total_return_pct')} | {m.get('max_drawdown_pct')} | "
                     f"{m.get('avg_days_held')} |")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
