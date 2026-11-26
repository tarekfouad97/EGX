# EGX Swing Scan - session 2026-11-26

_Generated 2026-11-27 00:05 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: RISK-OFF** | EGX30 50,312 (+3.7% 1M) - EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed

Scanned 239 stocks, 101 filtered out (currency/liquidity/volatility), **4 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.5 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **SDTI** | PULLBACK | 75 | 84.08 | 85.33 | 79.88 | 93.50 | 101.68 | 1.5R | 6.4% | 18 | 1,536 |
| 2 | **AMOC** | BOUNCE | 65 | 12.00 | 12.22 | 11.13 | 13.31 | 15.49 | 1.0R | 8.9% | 91 | 1,112 |
| 3 | **AMIA** | BOUNCE | 60 | 15.45 | 15.76 | 14.43 | 17.09 | 19.75 | 1.0R | 8.4% | 75 | 1,182 |
| 4 | **ADRI** | PULLBACK | 45 | 12.83 | 13.14 | 12.06 | 14.76 | 16.38 | 1.5R | 8.2% | 92 | 1,209 |

### 1. SDTI - Sharm Dreams Co. for Tourism Investment (PULLBACK)
Consumer Services | ATR 3.219 (3.8%/day) | ADV 15.7M EGP | RSI 50.5 | EMA10 84.057 | RS vs EGX30 -0.9pts

- Uptrend: EMA20 84.18 > EMA50 81.49 > SMA200 57.07
- Pulled back toward EMA20 84.18 (low 82.40)
- RSI 50 reset, Stoch %K 37 above %D 34 and rising
- ⚠ 1M high 90.99 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield 0.0% | D/E 3.29 | Net income n/a | Mkt cap 4.46B

### 2. AMOC - Alexandria Mineral Oils Co. (BOUNCE)
Energy Minerals | ATR 0.544 (4.5%/day) | ADV 123.6M EGP | RSI 35.0 | EMA10 12.585 | RS vs EGX30 -9.6pts

- Above SMA200 9.97 - long-term trend intact
- RSI 35 (prev 33) oversold and turning up
- Low 11.54 pierced lower Bollinger band 11.93
- ⚠ Earnings due 2026-12-02 - inside the holding window

**Fundamentals:** P/E 6.27 | P/B 2.89 | EPS 1.92 | ROE 47.1% | Div yield 10.1% | D/E 0.00 | Net income 1.33B | Mkt cap 15.50B | Next earnings 2026-12-02

### 3. AMIA - Arab Moltaqa Investments Company (BOUNCE)
Finance | ATR 0.823 (5.3%/day) | ADV 7.4M EGP | RSI 33.5 | EMA10 16.217 | RS vs EGX30 -11.1pts

- Above SMA200 11.43 - long-term trend intact
- RSI 33 (prev 33) oversold and turning up
- Low 15.05 pierced lower Bollinger band 15.26

**Fundamentals:** P/E 18.85 | P/B 6.03 | EPS 0.82 | ROE 28.7% | Div yield 0.7% | D/E 4.10 | Net income 0.27B | Mkt cap 7.89B

### 4. ADRI - Arab Development & Real Estate Investment (PULLBACK)
Finance | ATR 0.675 (5.3%/day) | ADV 29.6M EGP | RSI 50.4 | EMA10 12.826 | RS vs EGX30 -4.4pts

- Uptrend: EMA20 12.84 > EMA50 12.41 > SMA200 8.66
- Pulled back toward EMA20 12.84 (low 12.81)
- RSI 50 reset, Stoch %K 57 above %D 53 and rising
- ⚠ 1M high 13.72 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield n/a | D/E n/a | Net income n/a | Mkt cap n/a

## Data quality

Universe 296 | screener OK 239 | recovered from fallback 0 | dropped 57

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALEX: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, ema20, ema50, sma200 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- APPC: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- APPF: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-11-25)
- DCRC: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- EEP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EFAC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGOTH: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS30AJ1C016-EGP: stale bar 2026-11-25 (session 2026-11-26); fallback history too short
- EGS3E071C013-EGP: screener missing sma200; fallback history too short
- EGS48271C018-EGP: stale bar 2026-11-25 (session 2026-11-26); fallback history too short
- EGS65101C015: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65621C012: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65861C014: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS659O1C015: stale bar 2026-11-25 (session 2026-11-26); fallback history too short
- EGS72L31C011: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGWA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EITP: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- ELAB: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ENPI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GEOS: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GOUR: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- GROV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GTHE: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- HDST: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- IRAX: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- KNGC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- KORA: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- LKGP: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- MITR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MLIC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MMHC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NAMI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBCC: screener missing atr, ema20, ema50, sma200 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBKE: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- NCGC: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- NFCI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NMIN: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- OCAP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- PACH: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- PMSC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- POCO: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- RMTV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SIEG: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SINA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SMPP: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- SNFI: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- SPRK: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SUCE: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- TORA: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- WATP: stale bar 2026-11-25 (session 2026-11-26); fallback fetch failed (HTTP Error 404: Not Found)
- YAYT: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)

<details><summary>Run log</summary>

| Stage | Outcome | Detail |
|---|---|---|
| UNIVERSE | OK | 296 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-11-26 (newest trade in screener data) |
| VALIDATE | PARTIAL | 239 ready, 57 need recovery |
| RECOVER | PARTIAL | 0 recovered, 57 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/3 pullback candidates |
| SCAN | OK | 4 setups from 239 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
