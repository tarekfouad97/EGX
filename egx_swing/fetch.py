"""Live data from TradingView's Egypt screener (daily timeframe)."""

import json
import urllib.parse
import urllib.request

SCAN_URL = "https://scanner.tradingview.com/egypt/scan"

# screener column -> field name used by the rest of the package
COLUMNS = {
    "description": "name",
    "sector": "sector",
    "currency": "currency",
    "pricescale": "pricescale",        # tick = 1 / pricescale (0.01, or 0.001 under 1 EGP)
    "update_time": "update_time",      # unix time of the last trade = which session the bar is
    "close": "close",
    "open": "open",
    "high": "high",
    "low": "low",
    "EMA10": "ema10",
    "EMA20": "ema20",
    "EMA50": "ema50",
    "SMA200": "sma200",
    "RSI": "rsi",
    "RSI[1]": "rsi_prev",
    "MACD.macd": "macd",
    "MACD.signal": "macd_signal",
    "Stoch.K": "stoch_k",
    "Stoch.D": "stoch_d",
    # Stoch.K[1]/Stoch.D[1] are deliberately NOT used: the screener's values are inconsistent
    # with its own %D (=SMA3 of %K). Previous-bar Stoch comes from candle history instead.
    "BB.lower": "bb_lower",
    "ADX": "adx",
    "ADX+DI": "di_plus",
    "ADX-DI": "di_minus",
    "ATR": "atr",
    "Perf.1M": "perf_1m",
    "High.1M": "high_1m",
    "price_52_week_high": "high_52w",
    "volume": "volume",
    "average_volume_10d_calc": "vol_avg_10d",
    # fundamentals (often partly null for EGX names) - context for the AI review, never a filter
    "price_earnings_ttm": "pe_ratio",
    "price_book_ratio": "pb_ratio",
    "earnings_per_share_basic_ttm": "eps",
    "return_on_equity": "roe",
    "dividends_yield_current": "div_yield",
    "debt_to_equity": "debt_to_equity",
    "market_cap_calc": "market_cap",
    "net_income": "net_income",
    "total_revenue": "revenue",
    "earnings_release_next_date": "next_earnings",
}

INDEX_COLUMNS = {
    "close": "close",
    "EMA20": "ema20",
    "EMA50": "ema50",
    "SMA200": "sma200",
    "Perf.W": "perf_1w",
    "Perf.1M": "perf_1m",
    "RSI": "rsi",
}


def _post(payload, timeout=30):
    req = urllib.request.Request(
        SCAN_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (EGX-Swing/1.0)"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _rows(data, columns):
    keys = list(columns.values())
    out = []
    for row in data.get("data", []):
        rec = dict(zip(keys, row["d"]))
        rec["symbol"] = row["s"].split(":")[-1]
        out.append(rec)
    return out


def fetch_universe(top=500):
    """Primary common stocks on EGX, largest `top` by market cap (500 covers the whole exchange)."""
    payload = {
        "filter": [
            {"left": "is_primary", "operation": "equal", "right": True},
            {"left": "type", "operation": "equal", "right": "stock"},
        ],
        "options": {"lang": "en"},
        "columns": list(COLUMNS),
        "sort": {"sortBy": "market_cap_calc", "sortOrder": "desc"},
        "range": [0, top],
    }
    return _rows(_post(payload), COLUMNS)


def fetch_index(ticker="EGX:EGX30"):
    payload = {"symbols": {"tickers": [ticker]}, "columns": list(INDEX_COLUMNS)}
    rows = _rows(_post(payload), INDEX_COLUMNS)
    return rows[0] if rows else {}


# ───────────────────── fallback: Yahoo Finance daily candles ─────────────────────

YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=13mo&interval=1d"
YAHOO_INDEX = "^CASE30"


def fetch_history(symbol, timeout=20):
    """Daily candles for an EGX ticker (or the EGX30 index), oldest first, dated in Cairo time."""
    from datetime import datetime, timedelta, timezone
    sym = symbol if symbol.startswith("^") else f"{symbol}.CA"
    req = urllib.request.Request(YAHOO_URL.format(sym=urllib.parse.quote(sym)),
                                 headers={"User-Agent": "Mozilla/5.0 (EGX-Swing/1.0)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    res = (data.get("chart") or {}).get("result") or []
    if not res:
        return []
    r = res[0]
    offset = timedelta(seconds=r.get("meta", {}).get("gmtoffset", 7200))
    q = r["indicators"]["quote"][0]
    out = []
    for i, ts in enumerate(r.get("timestamp") or []):
        bar = {k: q[k][i] for k in ("open", "high", "low", "close", "volume")}
        if None in (bar["open"], bar["high"], bar["low"], bar["close"]):
            continue                                    # holiday/suspension gap
        bar["date"] = (datetime.fromtimestamp(ts, timezone.utc) + offset).date()
        out.append(bar)
    return out
