"""Fault-tolerant scan pipeline: a small state machine that always ends in a report.

Run stages (each one either succeeds, falls back, or degrades - never aborts):

    UNIVERSE --> INDEX --> SESSION --> VALIDATE --> RECOVER --> ENRICH --> SCAN --> DONE

    UNIVERSE  TradingView screener (retried)  -> cached universe list -> empty
    INDEX     TradingView EGX30 (retried)     -> EGX30 from Yahoo candles -> UNKNOWN regime
    SESSION   newest trade date in primary data -> EGX30 bar date -> newest recovered bar
    VALIDATE  every stock: complete and on the session date? -> READY, else NEEDS_RECOVERY
    RECOVER   Yahoo candles -> own indicators -> fresh and complete? -> RECOVERED, else DROPPED
    ENRICH    previous-bar Stoch for PULLBACK candidates from candles (optional)
    SCAN      setups.scan(); an unexpected error yields zero signals, not a crash
    AI_REVIEW fundamentals checks + Claude news/fundamentals verdict per pick;
              skipped without an API key, per-pick failures only add a warning

Per-stock states:  READY | RECOVERED | DROPPED(reason)

Every transition is recorded in `events`, which the report prints, so a degraded
run says exactly what happened and which stocks were dropped and why.
"""

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from . import ai_review
from . import fetch as _fetch
from . import indicators
from .setups import _num, pullback, scan

REQUIRED = ("close", "high", "low", "atr", "vol_avg_10d", "volume", "ema20", "ema50", "sma200",
            "rsi", "rsi_prev", "stoch_k", "stoch_d", "bb_lower", "adx", "di_plus", "di_minus", "high_1m")
META = ("symbol", "name", "sector", "currency", "pricescale")
# not price-derived, so kept from the screener row when price data is recovered elsewhere
CARRY = META + ai_review.FUNDAMENTAL_KEYS
INDEX_REQUIRED = ("close", "ema20", "ema50")

READY, RECOVERED, DROPPED = "READY", "RECOVERED", "DROPPED"



def _retry(fn, attempts=3, delay=2.0, sleep=time.sleep):
    err = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:          # network, HTTP, JSON - all retryable
            err = e
            if i < attempts - 1:
                sleep(delay * 2 ** i)
    raise err


def missing_fields(s, required=REQUIRED):
    return [k for k in required if not _num(s.get(k))]


def bar_date(s, to_cairo):
    if s.get("bar_date"):
        return s["bar_date"]
    t = s.get("update_time")
    if _num(t):
        return to_cairo(datetime.fromtimestamp(t, timezone.utc)).strftime("%Y-%m-%d")
    return None


class Run:
    def __init__(self, fetch=_fetch, cache_path=None, to_cairo=None, sleep=time.sleep, workers=8,
                 ai=True, ai_client=None, ai_max=8):
        self.fetch, self.cache_path, self.sleep, self.workers = fetch, cache_path, sleep, workers
        self.ai, self.ai_client, self.ai_max = ai, ai_client, ai_max
        self.to_cairo = to_cairo or (lambda dt: dt)
        self.events = []
        self.status = {}           # symbol -> {"state": ..., "source": ..., "reason": ...}

    def log(self, stage, outcome, detail=""):
        self.events.append({"stage": stage, "outcome": outcome, "detail": detail})

    def _history(self, symbol):
        return _retry(lambda: self.fetch.fetch_history(symbol), attempts=2, delay=1.0, sleep=self.sleep)

    # ── stages ──────────────────────────────────────────────────────────────

    def universe(self, top):
        try:
            stocks = _retry(lambda: self.fetch.fetch_universe(top), sleep=self.sleep)
            if not stocks:
                raise ValueError("screener returned 0 rows")
            self.log("UNIVERSE", "OK", f"{len(stocks)} stocks from TradingView")
            self._save_cache(stocks)
            return stocks, True
        except Exception as e:
            self.log("UNIVERSE", "FALLBACK", f"TradingView failed: {e}")
        cached = self._load_cache()
        if cached:
            self.log("UNIVERSE", "FALLBACK", f"{len(cached)} stocks from cached universe; all go to recovery")
            return [dict(m) for m in cached[:top]], False
        self.log("UNIVERSE", "FAILED", "no screener data and no cached universe")
        return [], False

    def index(self):
        try:
            idx = _retry(lambda: self.fetch.fetch_index(), sleep=self.sleep)
            if missing_fields(idx, INDEX_REQUIRED):
                raise ValueError(f"missing {missing_fields(idx, INDEX_REQUIRED)}")
            self.log("INDEX", "OK", "EGX30 from TradingView")
            return idx
        except Exception as e:
            self.log("INDEX", "FALLBACK", f"TradingView EGX30 failed: {e}")
        try:
            ind = indicators.compute(self._history(self.fetch.YAHOO_INDEX))
            if ind and not missing_fields(ind, INDEX_REQUIRED):
                self.log("INDEX", "RECOVERED", f"EGX30 computed from Yahoo candles ({ind['bar_date']})")
                return ind
            raise ValueError("history too short or incomplete")
        except Exception as e:
            self.log("INDEX", "DEGRADED", f"EGX30 unavailable ({e}); regime UNKNOWN, risk halved")
            return {}

    def session(self, stocks, index):
        dates = [d for d in (bar_date(s, self.to_cairo) for s in stocks) if d]
        if dates:
            d = max(dates)
            self.log("SESSION", "OK", f"{d} (newest trade in screener data)")
            return d
        if index.get("bar_date"):
            self.log("SESSION", "FALLBACK", f"{index['bar_date']} (EGX30 last bar)")
            return index["bar_date"]
        self.log("SESSION", "PENDING", "no dated primary data; will use newest recovered bar")
        return None

    def validate(self, stocks, session):
        ready, todo = [], []
        for s in stocks:
            sym = s.get("symbol")
            miss = missing_fields(s)
            d = bar_date(s, self.to_cairo)
            if len(miss) == len(REQUIRED):
                todo.append((s, "no screener data"))
            elif miss:
                todo.append((s, f"screener missing {', '.join(miss[:4])}{' ...' if len(miss) > 4 else ''}"))
            elif session and d != session:
                todo.append((s, f"stale bar {d or 'undated'} (session {session})"))
            else:
                ready.append(s)
                self.status[sym] = {"state": READY, "source": "tradingview"}
        self.log("VALIDATE", "OK" if not todo else "PARTIAL",
                 f"{len(ready)} ready, {len(todo)} need recovery")
        return ready, todo

    def recover(self, todo, session):
        def one(item):
            s, why = item
            try:
                ind = indicators.compute(self._history(s["symbol"]))
            except Exception as e:
                return s, None, f"{why}; fallback fetch failed ({e})"
            if not ind:
                return s, None, f"{why}; fallback history too short"
            return s, ind, why

        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            results = list(ex.map(one, todo))

        if session is None:
            dates = [ind["bar_date"] for _, ind, _ in results if ind]
            session = max(dates) if dates else None
            if session:
                self.log("SESSION", "FALLBACK", f"{session} (newest recovered bar)")

        recovered = []
        for s, ind, why in results:
            sym = s.get("symbol")
            if ind is None:
                self.status[sym] = {"state": DROPPED, "reason": why}
                continue
            if session and ind["bar_date"] != session:
                self.status[sym] = {"state": DROPPED,
                                    "reason": f"{why}; fallback also stale (last bar {ind['bar_date']})"}
                continue
            merged = {**{k: s.get(k) for k in CARRY if s.get(k) is not None}, **ind}
            miss = missing_fields(merged)
            if miss:
                self.status[sym] = {"state": DROPPED, "reason": f"{why}; fallback missing {', '.join(miss)}"}
                continue
            self.status[sym] = {"state": RECOVERED, "source": "yahoo", "reason": why}
            recovered.append(merged)
        dropped = len(results) - len(recovered)
        if results:
            self.log("RECOVER", "OK" if not dropped else "PARTIAL",
                     f"{len(recovered)} recovered, {dropped} dropped")
        return recovered, session

    def enrich(self, stocks, session):
        """Previous-bar Stoch for PULLBACK candidates (screener's [1] values are unreliable)."""
        need = [s for s in stocks if not _num(s.get("stoch_k_prev")) and pullback(s)]
        if not need:
            return

        def one(s):
            try:
                ind = indicators.compute(self._history(s["symbol"]))
                if ind and ind["bar_date"] == session:
                    s["stoch_k_prev"], s["stoch_d_prev"] = ind["stoch_k_prev"], ind["stoch_d_prev"]
                    return True
            except Exception:
                pass
            return False

        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            ok = sum(ex.map(one, need))
        self.log("ENRICH", "OK" if ok == len(need) else "PARTIAL",
                 f"previous-bar Stoch for {ok}/{len(need)} pullback candidates")

    def run(self, top, cfg):
        stocks, _ = self.universe(top)
        index = self.index()
        session = self.session(stocks, index)
        ready, todo = self.validate(stocks, session)
        recovered, session = self.recover(todo, session)
        tradeable = ready + recovered
        self.enrich(tradeable, session)
        try:
            result = scan(tradeable, index, cfg)
            self.log("SCAN", "OK", f"{len(result['signals'])} setups from {len(tradeable)} stocks")
        except Exception as e:
            self.log("SCAN", "FAILED", f"{type(e).__name__}: {e}")
            result = scan([], index, cfg)
        self.review(result, tradeable, session)
        result["as_of"] = session
        result["universe"] = len(stocks)
        result["data_status"] = self.status
        result["events"] = self.events
        result["run_status"] = self.run_status(tradeable)
        return result, index

    def review(self, result, tradeable, session):
        by_sym = {s.get("symbol"): s for s in tradeable}
        try:
            ai_review.apply(result, by_sym, session, self.log, client=self.ai_client,
                            max_reviews=self.ai_max, enabled=self.ai)
        except Exception as e:      # the review must never cost us the report
            result.setdefault("vetoed", [])
            result["ai_review"] = f"failed: {type(e).__name__}: {e}"
            self.log("AI_REVIEW", "FAILED", result["ai_review"])

    def run_status(self, tradeable):
        if not tradeable:
            return "FAILED"
        bad = {"FALLBACK", "DEGRADED", "FAILED", "PARTIAL", "PENDING"}
        if any(e["outcome"] in bad for e in self.events) or any(
                v["state"] == DROPPED for v in self.status.values()):
            return "DEGRADED"
        return "OK"

    # ── universe cache ─────────────────────────────────────────────────────

    def _save_cache(self, stocks):
        if not self.cache_path:
            return
        try:
            os.makedirs(os.path.dirname(self.cache_path) or ".", exist_ok=True)
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump([{k: s.get(k) for k in META} for s in stocks], f, indent=1, ensure_ascii=False)
        except Exception as e:
            self.log("UNIVERSE", "WARN", f"could not write cache: {e}")

    def _load_cache(self):
        if not self.cache_path:
            return None
        try:
            with open(self.cache_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
