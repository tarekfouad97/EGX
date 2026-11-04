# EGX Swing Scan - session 2026-11-04

_Generated 2026-11-04 22:14 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: RISK-OFF** | EGX30 50,650 (-6.1% 1M) - EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed

Scanned 256 stocks, 134 filtered out (currency/liquidity/volatility), **3 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.5 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **ADRI** | PULLBACK | 85 | 12.80 | 12.88 | 11.59 | 14.82 | 16.75 | 1.5R | 10.0% | 77 | 992 |
| 2 | **TALM** | PULLBACK | 80 | 19.60 | 19.78 | 18.53 | 21.66 | 23.53 | 1.5R | 6.3% | 80 | 1,582 |
| 3 | **AIH** | PULLBACK | 70 | 0.806 | 0.812 | 0.708 | 0.968 | 1.124 | 1.5R | 12.8% | 961 | 780 |

### 1. ADRI - Arab Development & Real Estate Investment (PULLBACK)
Finance | ATR 0.765 (6.0%/day) | ADV 37.4M EGP | RSI 51.6 | EMA10 12.676 | RS vs EGX30 +9.4pts

- Uptrend: EMA20 12.75 > EMA50 11.97 > SMA200 7.98
- Pulled back toward EMA20 12.75 (low 12.13)
- RSI 52 reset, Stoch %K 26 above %D 20 and rising
- ⚠ 1M high 14.7 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield n/a | D/E n/a | Net income n/a | Mkt cap n/a

### 2. TALM - Taaleem Management Services S.A.E (PULLBACK)
Consumer Services | ATR 1.237 (6.3%/day) | ADV 21.1M EGP | RSI 49.7 | EMA10 19.185 | RS vs EGX30 -1.8pts

- Uptrend: EMA20 19.52 > EMA50 19.51 > SMA200 16.90
- Pulled back toward EMA20 19.52 (low 19.15)
- RSI 50 reset, Stoch %K 49 above %D 41 and rising

**Fundamentals:** P/E 23.46 | P/B 8.52 | EPS 0.84 | ROE 29.1% | Div yield 0.0% | D/E 1.07 | Net income 0.62B | Mkt cap 14.39B

### 3. AIH - Arabia Investments Holding SAE (PULLBACK)
Finance | ATR 0.0451 (5.6%/day) | ADV 31.7M EGP | RSI 56.1 | EMA10 0.7767 | RS vs EGX30 +11.4pts

- Uptrend: EMA20 0.78 > EMA50 0.73 > SMA200 0.47
- Pulled back toward EMA20 0.78 (low 0.77)
- RSI 56 reset, Stoch %K 51 above %D 44 and rising
- ⚠ 1M high 0.913 sits below T1 - resistance
- ⚠ Loss-making (negative EPS/ROE/net income)

**Fundamentals:** P/E n/a | P/B n/a | EPS -0.15 | ROE -40.4% | Div yield 0.0% | D/E 7.13 | Net income -0.21B | Mkt cap 1.26B

## Data quality

Universe 295 | screener OK 256 | recovered from fallback 0 | dropped 39

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- BQDC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-11-03)
- EEP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EFAC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGOTH: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS3A0Y1C018: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
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
| UNIVERSE | OK | 295 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-11-04 (newest trade in screener data) |
| VALIDATE | PARTIAL | 256 ready, 39 need recovery |
| RECOVER | PARTIAL | 0 recovered, 39 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/9 pullback candidates |
| SCAN | OK | 3 setups from 256 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
