"""Indicators computed from daily OHLCV candles, matching TradingView's definitions.

Used when the screener's values for a stock are missing or stale and we fall
back to raw price history. Output keys are the same as fetch.COLUMNS values,
so recovered stocks flow through the scanner unchanged.

Definitions (TradingView defaults): EMA seeded with an SMA, Wilder smoothing
(RMA) for RSI/ATR/ADX, Stoch 14/3/3, MACD 12/26/9, Bollinger 20/2.
"""

from datetime import timedelta

MIN_BARS = 210          # SMA200 plus a little warm-up


def sma(xs, n):
    out = [None] * len(xs)
    for i in range(n - 1, len(xs)):
        out[i] = sum(xs[i - n + 1:i + 1]) / n
    return out


def _seeded(xs, n, alpha):
    out = [None] * len(xs)
    vals = [(i, x) for i, x in enumerate(xs) if x is not None]
    if len(vals) < n:
        return out
    start = vals[n - 1][0]
    prev = sum(x for _, x in vals[:n]) / n
    out[start] = prev
    for i in range(start + 1, len(xs)):
        if xs[i] is None:
            continue
        prev = alpha * xs[i] + (1 - alpha) * prev
        out[i] = prev
    return out


def ema(xs, n):
    return _seeded(xs, n, 2 / (n + 1))


def rma(xs, n):
    return _seeded(xs, n, 1 / n)


def rsi(closes, n=14):
    gains, losses = [None], [None]
    for a, b in zip(closes, closes[1:]):
        gains.append(max(b - a, 0.0))
        losses.append(max(a - b, 0.0))
    g, l = rma(gains, n), rma(losses, n)
    out = [None] * len(closes)
    for i in range(len(closes)):
        if g[i] is None or l[i] is None:
            continue
        out[i] = 100.0 if l[i] == 0 else 100 - 100 / (1 + g[i] / l[i])
    return out


def stoch(highs, lows, closes, n=14, k_smooth=3, d_smooth=3):
    raw = [None] * len(closes)
    for i in range(n - 1, len(closes)):
        hh, ll = max(highs[i - n + 1:i + 1]), min(lows[i - n + 1:i + 1])
        raw[i] = 100 * (closes[i] - ll) / (hh - ll) if hh > ll else 50.0
    k = _sma_opt(raw, k_smooth)
    return k, _sma_opt(k, d_smooth)


def _sma_opt(xs, n):
    out = [None] * len(xs)
    for i in range(len(xs)):
        win = xs[max(0, i - n + 1):i + 1]
        if len(win) == n and None not in win:
            out[i] = sum(win) / n
    return out


def true_range(highs, lows, closes):
    tr = [highs[0] - lows[0]]
    for i in range(1, len(closes)):
        tr.append(max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])))
    return tr


def adx(highs, lows, closes, n=14):
    pdm, mdm = [None], [None]
    for i in range(1, len(closes)):
        up, down = highs[i] - highs[i - 1], lows[i - 1] - lows[i]
        pdm.append(up if up > down and up > 0 else 0.0)
        mdm.append(down if down > up and down > 0 else 0.0)
    tr = [None] + true_range(highs, lows, closes)[1:]
    atr_, p, m = rma(tr, n), rma(pdm, n), rma(mdm, n)
    dip, dim, dx = [None] * len(closes), [None] * len(closes), [None] * len(closes)
    for i in range(len(closes)):
        if atr_[i]:
            dip[i], dim[i] = 100 * p[i] / atr_[i], 100 * m[i] / atr_[i]
            s = dip[i] + dim[i]
            dx[i] = 100 * abs(dip[i] - dim[i]) / s if s else 0.0
    return rma(dx, n), dip, dim


def _months_back(d, n):
    y, m = divmod(d.year * 12 + d.month - 1 - n, 12)
    for day in (d.day, 30, 29, 28):
        try:
            return d.replace(year=y, month=m + 1, day=day)
        except ValueError:
            continue


def compute(candles):
    """candles: list of dicts {date, open, high, low, close, volume}, oldest first.

    Returns the indicator dict for the last bar, or None if history is too short.
    """
    if len(candles) < MIN_BARS:
        return None
    o = [c["open"] for c in candles]
    h = [c["high"] for c in candles]
    lo = [c["low"] for c in candles]
    c = [c_["close"] for c_ in candles]
    v = [c_["volume"] or 0 for c_ in candles]
    last = candles[-1]["date"]

    ema12, ema26 = ema(c, 12), ema(c, 26)
    macd_line = [a - b if a is not None and b is not None else None for a, b in zip(ema12, ema26)]
    rsi_ = rsi(c)
    k, d = stoch(h, lo, c)
    basis = sma(c, 20)
    win = c[-20:]
    sd = (sum((x - basis[-1]) ** 2 for x in win) / 20) ** 0.5
    adx_, dip, dim = adx(h, lo, c)
    atr_ = rma(true_range(h, lo, c), 14)

    month_ago = _months_back(last, 1)
    year_ago = last - timedelta(days=365)
    ref = [x["close"] for x in candles if x["date"] < month_ago]     # TradingView Perf.1M convention
    m_highs = [x["high"] for x in candles if x["date"] > month_ago]
    y_highs = [x["high"] for x in candles if x["date"] > year_ago]

    return {
        "bar_date": last.isoformat(),
        "open": o[-1], "high": h[-1], "low": lo[-1], "close": c[-1],
        "ema10": ema(c, 10)[-1], "ema20": ema(c, 20)[-1], "ema50": ema(c, 50)[-1],
        "sma200": sma(c, 200)[-1],
        "rsi": rsi_[-1], "rsi_prev": rsi_[-2],
        "macd": macd_line[-1], "macd_signal": ema(macd_line, 9)[-1],
        "stoch_k": k[-1], "stoch_d": d[-1], "stoch_k_prev": k[-2], "stoch_d_prev": d[-2],
        "bb_lower": basis[-1] - 2 * sd,
        "adx": adx_[-1], "di_plus": dip[-1], "di_minus": dim[-1],
        "atr": atr_[-1],
        "perf_1m": (c[-1] / ref[-1] - 1) * 100 if ref else None,
        "high_1m": max(m_highs), "high_52w": max(y_highs),
        "volume": v[-1], "vol_avg_10d": sum(v[-10:]) / 10,
    }
