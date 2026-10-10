"""Command-line entry point: python -m egx_swing [options]"""

import argparse
import json
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from . import fetch, report
from .setups import DEFAULTS, scan


def cairo_now():
    return datetime.now(ZoneInfo("Africa/Cairo"))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="egx_swing", description="EGX swing-trade setup scanner")
    ap.add_argument("--top", type=int, default=100, help="universe size by market cap (default 100)")
    ap.add_argument("--capital", type=float, default=DEFAULTS["capital"], help="account size in EGP")
    ap.add_argument("--risk-pct", type=float, default=DEFAULTS["risk_pct"], help="%% of capital risked per trade")
    ap.add_argument("--min-adv", type=float, default=DEFAULTS["min_adv_egp"], help="min avg daily value traded, EGP")
    ap.add_argument("--out-dir", help="write <date>.md, <date>.json and latest.md here")
    ap.add_argument("--input", help="offline: JSON file with {\"stocks\": [...], \"index\": {...}}")
    ap.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    args = ap.parse_args(argv)

    if args.input:
        with open(args.input) as f:
            snap = json.load(f)
        stocks, index = snap["stocks"], snap.get("index", {})
    else:
        try:
            stocks = fetch.fetch_universe(args.top)
            index = fetch.fetch_index()
        except Exception as e:
            print(f"ERROR fetching TradingView data: {e}", file=sys.stderr)
            return 1
        if not stocks:
            print("ERROR: screener returned no stocks", file=sys.stderr)
            return 1

    cfg = {"capital": args.capital, "risk_pct": args.risk_pct, "min_adv_egp": args.min_adv}
    result = scan(stocks, index, cfg)

    now = cairo_now()
    md = report.render(result, index, now.strftime("%Y-%m-%d %H:%M Cairo"))
    if now.weekday() in (6, 0, 1, 2, 3) and (now.hour, now.minute) < (14, 45) and not args.input:
        md = md.replace("\n", "\n> ⚠ EGX session may still be open - today's bar is not final.\n", 1)

    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)
        day = now.strftime("%Y-%m-%d")
        with open(os.path.join(args.out_dir, f"{day}.md"), "w") as f:
            f.write(md)
        with open(os.path.join(args.out_dir, "latest.md"), "w") as f:
            f.write(md)
        with open(os.path.join(args.out_dir, f"{day}.json"), "w") as f:
            json.dump({"date": day, "index": index, **result}, f, indent=2)

    print(json.dumps(result, indent=2) if args.json else md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
