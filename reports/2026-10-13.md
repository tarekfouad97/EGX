# EGX Swing Scan - session 2026-10-13

_Generated 2026-10-13 22:43 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: RISK-OFF** | EGX30 51,265 (-8.8% 1M) - EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed

Scanned 237 stocks, 105 filtered out (currency/liquidity/volatility), **5 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.5 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **CANA** | PULLBACK | 80 | 44.85 | 45.21 | 41.99 | 50.04 | 54.87 | 1.5R | 7.1% | 31 | 1,402 |
| 2 | **RMDA** | BOUNCE | 55 | 5.22 | 5.29 | 4.69 | 5.89 | 7.09 | 1.0R | 11.3% | 166 | 878 |
| 3 | **EGAS** | BOUNCE | 55 | 51.40 | 54.18 | 45.99 | 62.37 | 78.75 | 1.0R | 15.1% | 12 | 650 |
| 4 | **ADIB** | BOUNCE | 50 | 44.50 | 46.35 | 42.38 | 50.32 | 58.26 | 1.0R | 8.6% | 25 | 1,159 |
| 5 | **CCRS** | BOUNCE | 50 | 2.08 | 2.16 | 1.75 | 2.57 | 3.39 | 1.0R | 19.0% | 243 | 525 |

### 1. CANA - Suez Canal Bank SAE (PULLBACK)
Finance | ATR 2.010 (4.5%/day) | ADV 15.9M EGP | RSI 52.2 | EMA10 44.858 | RS vs EGX30 +13.1pts

- Uptrend: EMA20 44.74 > EMA50 43.00 > SMA200 34.05
- Pulled back toward EMA20 44.74 (low 43.10)
- RSI 52 reset, Stoch %K 26 above %D 19 and rising

**Fundamentals:** P/E 7.55 | P/B 2.21 | EPS 5.94 | ROE 33.3% | Div yield 0.0% | D/E 2.38 | Net income 5.65B | Mkt cap 44.85B | Next earnings 2026-12-02

### 2. RMDA - Tenth of Ramadan Pharmaceutical Industries & Diagnostic-Rameda (BOUNCE)
Health Technology | ATR 0.281 (5.4%/day) | ADV 23.6M EGP | RSI 35.7 | EMA10 5.367 | RS vs EGX30 -8.1pts

- Above SMA200 4.74 - long-term trend intact
- RSI 36 (prev 30) oversold and turning up
- Low 4.91 within 1% of lower Bollinger band 4.90

**Fundamentals:** P/E 30.81 | P/B 3.64 | EPS 0.17 | ROE 15.2% | Div yield 0.6% | D/E 1.04 | Net income 0.27B | Mkt cap 10.61B | Next earnings 2026-12-02

### 3. EGAS - Egypt Gas Co. (BOUNCE)
Utilities | ATR 2.776 (5.4%/day) | ADV 5.7M EGP | RSI 33.3 | EMA10 54.596 | RS vs EGX30 -3.3pts

- Above SMA200 48.81 - long-term trend intact
- RSI 33 (prev 32) oversold and turning up
- Low 48.08 pierced lower Bollinger band 52.11
- ⚠ 1M high 60.94 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B 1.56 | EPS n/a | ROE n/a | Div yield 1.0% | D/E 0.21 | Net income 0.31B | Mkt cap 7.41B

### 4. ADIB - Abu Dhabi Islamic Bank-Egypt (BOUNCE)
Finance | ATR 1.493 (3.4%/day) | ADV 67.1M EGP | RSI 23.9 | EMA10 47.739 | RS vs EGX30 -6.4pts

- Above SMA200 44.03 - long-term trend intact
- RSI 24 (prev 27) oversold, still falling; Stoch %K 5 > %D 4
- Low 43.50 pierced lower Bollinger band 45.19

**Fundamentals:** P/E 4.31 | P/B 1.54 | EPS 10.32 | ROE 42.8% | Div yield 0.0% | D/E 0.46 | Net income 12.59B | Mkt cap 66.75B | Next earnings 2026-12-02

### 5. CCRS - Gulf Canadian Real Estate Investment Co. (BOUNCE)
Finance | ATR 0.155 (7.4%/day) | ADV 7.1M EGP | RSI 31.6 | EMA10 2.267 | RS vs EGX30 -10.9pts

- Above SMA200 2.03 - long-term trend intact
- RSI 32 (prev 32) oversold, still falling; Stoch %K 12 > %D 11
- Low 1.87 pierced lower Bollinger band 2.06

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield 0.0% | D/E 0.00 | Net income n/a | Mkt cap 0.44B

## Data quality

Universe 293 | screener OK 237 | recovered from fallback 0 | dropped 56

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALEX: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- APPC: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-10-12)
- DCRC: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- EEP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EFAC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGOTH: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS30AJ1C016-EGP: stale bar 2026-10-12 (session 2026-10-13); fallback history too short
- EGS3E071C013-EGP: screener missing ema50, sma200; fallback history too short
- EGS48271C018-EGP: stale bar 2026-10-12 (session 2026-10-13); fallback history too short
- EGS65101C015: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65621C012: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65861C014: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS659O1C015: stale bar 2026-10-12 (session 2026-10-13); fallback history too short
- EGS72L31C011: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGWA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EITP: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- ELAB: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ENPI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GEOS: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GOUR: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- GROV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GTHE: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- HALN: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- HDST: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- IRAX: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- KNGC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- KORA: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- LKGP: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- MITR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MLIC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MMHC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NAMI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBKE: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- NCGC: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- NFCI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NMIN: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- OCAP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- PACH: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- PMSC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- POCO: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- RMTV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SIEG: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SINA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SMPP: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- SNFI: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- SUCE: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- TORA: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- WATP: stale bar 2026-10-12 (session 2026-10-13); fallback fetch failed (HTTP Error 404: Not Found)
- YAYT: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)

<details><summary>Run log</summary>

| Stage | Outcome | Detail |
|---|---|---|
| UNIVERSE | OK | 293 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-10-13 (newest trade in screener data) |
| VALIDATE | PARTIAL | 237 ready, 56 need recovery |
| RECOVER | PARTIAL | 0 recovered, 56 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/3 pullback candidates |
| SCAN | OK | 5 setups from 237 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
