# EGX Swing Scan - session 2026-10-25

_Generated 2026-10-25 19:57 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: RISK-OFF** | EGX30 49,234 (-9.3% 1M) - EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed

Scanned 237 stocks, 138 filtered out (currency/liquidity/volatility), **2 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.5 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **HDBK** | PULLBACK | 75 | 103.66 | 105.52 | 79.92 | 143.92 | 182.32 | 1.5R | 24.3% | 3 | 317 |
| 2 | **SDTI** | PULLBACK | 75 | 81.83 | 83.38 | 73.13 | 98.76 | 114.13 | 1.5R | 12.3% | 9 | 750 |

### 1. HDBK - Housing & Development Bank (PULLBACK)
Finance | ATR 6.171 (6.0%/day) | ADV 24.5M EGP | RSI 50.3 | EMA10 100.236 | RS vs EGX30 +1.8pts

- Uptrend: EMA20 102.79 > EMA50 101.62 > SMA200 75.62
- Pulled back toward EMA20 102.79 (low 83.01)
- RSI 50 reset, Stoch %K 43 above %D 32 and rising
- ⚠ 1M high 113.99 sits below T1 - resistance

**Fundamentals:** P/E 5.54 | P/B 2.59 | EPS 18.73 | ROE 49.7% | Div yield 4.3% | D/E 0.03 | Net income 18.68B | Mkt cap 110.15B | Next earnings 2026-12-02

### 2. SDTI - Sharm Dreams Co. for Tourism Investment (PULLBACK)
Consumer Services | ATR 3.757 (4.6%/day) | ADV 17.9M EGP | RSI 51.2 | EMA10 83.374 | RS vs EGX30 +14.8pts

- Uptrend: EMA20 82.62 > EMA50 76.73 > SMA200 50.04
- Pulled back toward EMA20 82.62 (low 75.01)
- RSI 51 reset, Stoch %K 27 above %D 25 and rising
- ⚠ 1M high 94.9 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield 0.0% | D/E 3.29 | Net income n/a | Mkt cap 4.34B

## Data quality

Universe 291 | screener OK 237 | recovered from fallback 0 | dropped 54

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALEX: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- APPC: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-10-22)
- DCRC: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- EEP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EFAC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGOTH: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS30AJ1C016-EGP: stale bar 2026-10-21 (session 2026-10-25); fallback history too short
- EGS3E071C013-EGP: screener missing sma200; fallback history too short
- EGS48271C018-EGP: stale bar 2026-10-21 (session 2026-10-25); fallback history too short
- EGS65101C015: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65621C012: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65861C014: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS659O1C015: stale bar 2026-10-21 (session 2026-10-25); fallback history too short
- EGS72L31C011: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGWA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EITP: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- ELAB: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ENPI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GEOS: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GOUR: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- GROV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GTHE: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- HDST: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- IRAX: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- KNGC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- KORA: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- LKGP: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- MITR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MLIC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MMHC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NAMI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBKE: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- NCGC: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- NFCI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NMIN: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- OCAP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- PACH: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- PMSC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- POCO: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SIEG: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SINA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SMPP: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- SNFI: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- SUCE: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- TORA: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- WATP: stale bar 2026-10-21 (session 2026-10-25); fallback fetch failed (HTTP Error 404: Not Found)
- YAYT: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)

<details><summary>Run log</summary>

| Stage | Outcome | Detail |
|---|---|---|
| UNIVERSE | OK | 291 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-10-25 (newest trade in screener data) |
| VALIDATE | PARTIAL | 237 ready, 54 need recovery |
| RECOVER | PARTIAL | 0 recovered, 54 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/3 pullback candidates |
| SCAN | OK | 2 setups from 237 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
