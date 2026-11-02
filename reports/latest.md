# EGX Swing Scan - session 2026-11-02

_Generated 2026-11-02 19:35 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: RISK-OFF** | EGX30 48,403 (-6.7% 1M) - EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed

Scanned 256 stocks, 142 filtered out (currency/liquidity/volatility), **3 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.5 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **ADRI** | PULLBACK | 90 | 12.51 | 12.75 | 11.54 | 14.56 | 16.38 | 1.5R | 9.5% | 82 | 1,046 |
| 2 | **AIH** | PULLBACK | 75 | 0.751 | 0.775 | 0.702 | 0.884 | 0.994 | 1.5R | 9.4% | 1,369 | 1,061 |
| 3 | **SDTI** | PULLBACK | 75 | 81.55 | 84.32 | 75.84 | 97.04 | 109.76 | 1.5R | 10.1% | 11 | 928 |

### 1. ADRI - Arab Development & Real Estate Investment (PULLBACK)
Finance | ATR 0.780 (6.2%/day) | ADV 35.8M EGP | RSI 48.3 | EMA10 12.763 | RS vs EGX30 +11.9pts

- Uptrend: EMA20 12.81 > EMA50 11.93 > SMA200 7.90
- Pulled back toward EMA20 12.81 (low 12.11)
- RSI 48 reset, Stoch %K 16 above %D 16 and rising

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield n/a | D/E n/a | Net income n/a | Mkt cap n/a

### 2. AIH - Arabia Investments Holding SAE (PULLBACK)
Finance | ATR 0.0466 (6.2%/day) | ADV 32.4M EGP | RSI 47.1 | EMA10 0.7702 | RS vs EGX30 +8.1pts

- Uptrend: EMA20 0.77 > EMA50 0.73 > SMA200 0.47
- Pulled back toward EMA20 0.77 (low 0.73)
- RSI 47 reset, Stoch %K 39 above %D 35 and rising
- ⚠ Loss-making (negative EPS/ROE/net income)

**Fundamentals:** P/E n/a | P/B n/a | EPS -0.15 | ROE -40.4% | Div yield 0.0% | D/E 7.13 | Net income -0.21B | Mkt cap 1.17B

### 3. SDTI - Sharm Dreams Co. for Tourism Investment (PULLBACK)
Consumer Services | ATR 3.976 (4.9%/day) | ADV 15.8M EGP | RSI 49.7 | EMA10 82.404 | RS vs EGX30 +4.1pts

- Uptrend: EMA20 82.32 > EMA50 77.84 > SMA200 51.73
- Pulled back toward EMA20 82.32 (low 81.51)
- RSI 50 reset, Stoch %K 54 above %D 49 and rising
- ⚠ 1M high 90.85 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield 0.0% | D/E 3.29 | Net income n/a | Mkt cap 4.32B

## Data quality

Universe 294 | screener OK 256 | recovered from fallback 0 | dropped 38

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- BQDC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-11-01)
- EEP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EFAC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGOTH: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS3E071C013-EGP: screener missing sma200; fallback history too short
- EGS65101C015: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65621C012: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65861C014: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS72L31C011: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGWA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ELAB: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ENPI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GEOS: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GOUR: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- GROV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- HDST: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- KNGC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- KORA: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- MITR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MLIC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MMHC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NAMI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NFCI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NMIN: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- OCAP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- PMSC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- POCO: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- RMTV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SIEG: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SINA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- YAYT: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)

<details><summary>Run log</summary>

| Stage | Outcome | Detail |
|---|---|---|
| UNIVERSE | OK | 294 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-11-02 (newest trade in screener data) |
| VALIDATE | PARTIAL | 256 ready, 38 need recovery |
| RECOVER | PARTIAL | 0 recovered, 38 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/5 pullback candidates |
| SCAN | OK | 3 setups from 256 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
