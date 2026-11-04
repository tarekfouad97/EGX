"""Download daily OHLCV history for EGX symbols from TradingView's chart websocket.

This is the same feed the TradingView website uses. Bars are split-adjusted.
One CSV per symbol is written to the cache folder (date,open,high,low,close,volume),
so a backtest can be re-run offline without downloading again.

Needs only the Python standard library (uses websocket-client if it happens to be installed).

Usage:
    python -m backtest.tvfetch --bars 800 --out data/history            # every symbol in data/universe.json + EGX30
    python -m backtest.tvfetch --symbols COMI,SWDY --bars 800 --out data/history
"""

import argparse
import csv
import json
import time
from pathlib import Path

from egx_swing.tvhistory import fetch_one as _fetch


def fetch_one(symbol, bars=800, timeout=20):
    rows = _fetch(symbol, bars, timeout)
    return [{**r, "date": r["date"].isoformat()} for r in rows]


def save(path, candles):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "open", "high", "low", "close", "volume"])
        w.writeheader()
        w.writerows(candles)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--symbols", help="comma-separated; default = data/universe.json (EGP stocks) + EGX30")
    ap.add_argument("--universe", default="data/universe.json")
    ap.add_argument("--bars", type=int, default=800, help="daily bars per symbol (~250 per year)")
    ap.add_argument("--out", default="data/history")
    ap.add_argument("--skip-existing", action="store_true")
    a = ap.parse_args(argv)

    if a.symbols:
        syms = a.symbols.split(",")
    else:
        uni = json.load(open(a.universe))
        syms = ["EGX30"] + [u["symbol"] for u in uni if u.get("currency", "EGP") == "EGP"]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    ok, failed = 0, []
    for i, s in enumerate(syms, 1):
        p = out / f"{s}.csv"
        if a.skip_existing and p.exists():
            continue
        for attempt in range(3):
            try:
                c = fetch_one(s, a.bars)
                save(p, c)
                ok += 1
                break
            except Exception as e:  # network hiccup or unknown symbol
                err = str(e)
                time.sleep(1 + attempt)
        else:
            failed.append(f"{s}: {err}")
        if i % 25 == 0:
            print(f"{i}/{len(syms)} done", flush=True)
        time.sleep(0.3)
    print(f"saved {ok} symbols to {out}; failed {len(failed)}")
    for f in failed:
        print("  FAILED", f)


if __name__ == "__main__":
    main()
