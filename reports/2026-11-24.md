# EGX Swing Scan - session 2026-11-24

_Generated 2026-11-25 00:53 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: RISK-OFF** | EGX30 50,885 (-0.3% 1M) - EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed

Scanned 239 stocks, 95 filtered out (currency/liquidity/volatility), **3 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.5 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **SDTI** | PULLBACK | 75 | 85.01 | 88.19 | 79.64 | 101.01 | 113.84 | 1.5R | 9.7% | 11 | 970 |
| 2 | **ADRI** | PULLBACK | 55 | 12.94 | 13.07 | 12.00 | 14.68 | 16.28 | 1.5R | 8.2% | 93 | 1,216 |
| 3 | **AMIA** | BOUNCE | 50 | 15.74 | 16.38 | 14.95 | 17.81 | 20.67 | 1.0R | 8.7% | 69 | 1,130 |

### 1. SDTI - Sharm Dreams Co. for Tourism Investment (PULLBACK)
Consumer Services | ATR 3.309 (3.9%/day) | ADV 17.8M EGP | RSI 52.9 | EMA10 84.157 | RS vs EGX30 +3.7pts

- Uptrend: EMA20 84.26 > EMA50 81.30 > SMA200 56.50
- Pulled back toward EMA20 84.26 (low 84.00)
- RSI 53 reset, Stoch %K 28 above %D 19 and rising
- ⚠ 1M high 90.99 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield 0.0% | D/E 3.29 | Net income n/a | Mkt cap 4.50B

### 2. ADRI - Arab Development & Real Estate Investment (PULLBACK)
Finance | ATR 0.725 (5.6%/day) | ADV 30.8M EGP | RSI 51.6 | EMA10 12.802 | RS vs EGX30 -3.9pts

- Uptrend: EMA20 12.83 > EMA50 12.37 > SMA200 8.58
- Pulled back toward EMA20 12.83 (low 12.61)
- RSI 52 reset, Stoch %K 46 above %D 43 and rising
- ⚠ 1M high 13.72 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield n/a | D/E n/a | Net income n/a | Mkt cap n/a

### 3. AMIA - Arab Moltaqa Investments Company (BOUNCE)
Finance | ATR 0.854 (5.4%/day) | ADV 11.2M EGP | RSI 34.9 | EMA10 16.612 | RS vs EGX30 -10.8pts

- Above SMA200 11.32 - long-term trend intact
- RSI 35 (prev 38) oversold, still falling; Stoch %K 21 > %D 19
- Low 15.60 pierced lower Bollinger band 15.79

**Fundamentals:** P/E 19.20 | P/B 6.14 | EPS 0.82 | ROE 28.7% | Div yield 0.6% | D/E 4.10 | Net income 0.27B | Mkt cap 8.04B

## Data quality

Universe 295 | screener OK 239 | recovered from fallback 0 | dropped 56

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALEX: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- APPC: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- APPF: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-11-23)
- DCRC: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- EEP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EFAC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGOTH: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS30AJ1C016-EGP: stale bar 2026-11-23 (session 2026-11-24); fallback history too short
- EGS3E071C013-EGP: screener missing sma200; fallback history too short
- EGS48271C018-EGP: stale bar 2026-11-23 (session 2026-11-24); fallback history too short
- EGS65101C015: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65621C012: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65861C014: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS659O1C015: stale bar 2026-11-23 (session 2026-11-24); fallback history too short
- EGS72L31C011: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGWA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EITP: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- ELAB: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ENPI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GEOS: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GOUR: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- GROV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GTHE: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- HDST: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- IRAX: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- KNGC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- KORA: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- LKGP: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- MITR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MLIC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MMHC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NAMI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBKE: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- NCGC: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- NFCI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NMIN: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- OCAP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- PACH: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- PMSC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- POCO: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- RMTV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SIEG: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SINA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SMPP: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- SNFI: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- SUCE: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- TORA: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- WATP: stale bar 2026-11-23 (session 2026-11-24); fallback fetch failed (HTTP Error 404: Not Found)
- YAYT: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)

<details><summary>Run log</summary>

| Stage | Outcome | Detail |
|---|---|---|
| UNIVERSE | OK | 295 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-11-24 (newest trade in screener data) |
| VALIDATE | PARTIAL | 239 ready, 56 need recovery |
| RECOVER | PARTIAL | 0 recovered, 56 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/3 pullback candidates |
| SCAN | OK | 3 setups from 239 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
