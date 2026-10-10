#!/usr/bin/env python3
"""Print the parts of an EGX swing report the review needs, as compact JSON.

Usage: python3 picks.py <path-to-latest.json>
The full report also carries per-stock data status for ~100 stocks; this keeps
only the run header, the picks, the AI vetoes and anything that went wrong.
"""

import json
import sys

KEEP = ("symbol", "name", "sector", "setup", "quality", "close", "entry", "stop", "t1", "t2", "rr_t1",
        "risk_pct_of_price", "shares", "position_egp", "risk_egp", "rsi", "rs_vs_egx30", "atr_pct",
        "adv_egp", "reasons", "warnings", "notes", "fundamentals", "ai")


def main(path):
    with open(path, encoding="utf-8") as f:
        r = json.load(f)
    idx = r.get("index") or {}
    out = {
        "session": r.get("as_of"),
        "run_status": r.get("run_status"),
        "intraday": r.get("intraday"),
        "regime": r.get("regime"),
        "egx30": {k: idx.get(k) for k in ("close", "perf_1m", "ema20", "ema50")},
        "config": r.get("config"),
        "workflow_ai_review": r.get("ai_review"),
        "picks": [{k: s.get(k) for k in KEEP} for s in r.get("signals", [])],
        "vetoed_in_workflow": [{k: s.get(k) for k in KEEP} for s in r.get("vetoed", [])],
        "dropped": {k: v.get("reason") for k, v in (r.get("data_status") or {}).items()
                    if v.get("state") == "DROPPED"},
        "problems": [e for e in r.get("events", []) if e.get("outcome") not in ("OK",)],
    }
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
    print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
