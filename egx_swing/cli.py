"""Command-line entry point: python -m egx_swing [options]"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

from . import report
from .pipeline import Run
from .setups import DEFAULTS, scan

try:
    from zoneinfo import ZoneInfo
    CAIRO = ZoneInfo("Africa/Cairo")
except Exception:            # no IANA tz database (e.g. Windows without tzdata)
    CAIRO = None


def _last_weekday(year, month, weekday):
    d = datetime(year + (month == 12), month % 12 + 1, 1) - timedelta(days=1)
    while d.weekday() != weekday:
        d -= timedelta(days=1)
    return d


def _cairo_offset(utc):
    # Egypt DST: last Friday of April to last Thursday of October (UTC+3), else UTC+2.
    start = _last_weekday(utc.year, 4, 4)
    end = _last_weekday(utc.year, 10, 3) + timedelta(days=1)
    return 3 if start <= utc.replace(tzinfo=None) < end else 2


def to_cairo(utc):
    if CAIRO:
        return utc.astimezone(CAIRO)
    return utc.astimezone(timezone(timedelta(hours=_cairo_offset(utc))))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="egx_swing", description="EGX swing-trade setup scanner")
    ap.add_argument("--top", type=int, default=100, help="universe size by market cap (default 100)")
    ap.add_argument("--capital", type=float, default=float(DEFAULTS["capital"]), help="account size in EGP")
    ap.add_argument("--risk-pct", type=float, default=float(DEFAULTS["risk_pct"]),
                    help="%% of capital risked per trade")
    ap.add_argument("--min-adv", type=float, default=float(DEFAULTS["min_adv_egp"]),
                    help="min avg daily value traded, EGP")
    ap.add_argument("--out-dir", help="write <session-date>.md, <session-date>.json and latest.md here")
    ap.add_argument("--input", help="offline: JSON file with {\"stocks\": [...], \"index\": {...}}")
    ap.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    ap.add_argument("--cache", default=os.path.join("data", "universe.json"),
                    help="universe list kept for when the screener is down (default data/universe.json)")
    args = ap.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    cfg = {"capital": args.capital, "risk_pct": args.risk_pct, "min_adv_egp": args.min_adv}
    now = to_cairo(datetime.now(timezone.utc))
    index = {}
    try:
        if args.input:
            with open(args.input, encoding="utf-8") as f:
                snap = json.load(f)
            index = snap.get("index", {})
            result = scan(snap["stocks"], index, cfg)
            result.update(as_of=snap.get("as_of"), run_status="OFFLINE", events=[], data_status={})
        else:
            result, index = Run(cache_path=args.cache, to_cairo=to_cairo).run(args.top, cfg)
    except Exception as e:      # last resort: a bug, not a data problem - still publish a report
        result = scan([], {}, cfg)
        result.update(as_of=None, run_status="FAILED", data_status={},
                      events=[{"stage": "RUN", "outcome": "FAILED", "detail": f"{type(e).__name__}: {e}"}])
    result["intraday"] = (not args.input and result.get("as_of") == now.strftime("%Y-%m-%d")
                          and (now.hour, now.minute) < (14, 45))
    md = report.render(result, index, now.strftime("%Y-%m-%d %H:%M Cairo"))
    print(f"run status: {result['run_status']}", file=sys.stderr)

    if args.out_dir:
        if args.input:
            print("ERROR: --out-dir with --input would overwrite live reports; use --json or stdout",
                  file=sys.stderr)
            return 2
        # a run with no known session must not overwrite a good dated report
        day = result.get("as_of") or now.strftime("%Y-%m-%d") + "-FAILED"
        os.makedirs(args.out_dir, exist_ok=True)
        for name in (f"{day}.md", "latest.md"):
            with open(os.path.join(args.out_dir, name), "w", encoding="utf-8") as f:
                f.write(md)
        with open(os.path.join(args.out_dir, f"{day}.json"), "w", encoding="utf-8") as f:
            json.dump({"date": day, "index": index, **result}, f, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else md)
    return 0
