# EGX Swing Scan - session 2026-11-03

_Generated 2026-11-03 21:56 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: RISK-OFF** | EGX30 49,256 (-7.5% 1M) - EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed

Scanned 238 stocks, 125 filtered out (currency/liquidity/volatility), **3 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.5 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **AIH** | PULLBACK | 85 | 0.770 | 0.780 | 0.705 | 0.892 | 1.005 | 1.5R | 9.6% | 1,333 | 1,040 |
| 2 | **ADRI** | PULLBACK | 75 | 12.13 | 12.85 | 11.55 | 14.80 | 16.75 | 1.5R | 10.1% | 76 | 977 |
| 3 | **AJWA** | PULLBACK | 65 | 213.45 | 218.04 | 191.46 | 257.91 | 297.78 | 1.5R | 12.2% | 3 | 654 |

### 1. AIH - Arabia Investments Holding SAE (PULLBACK)
Finance | ATR 0.0457 (5.9%/day) | ADV 32.6M EGP | RSI 50.4 | EMA10 0.7702 | RS vs EGX30 +11.1pts

- Uptrend: EMA20 0.77 > EMA50 0.73 > SMA200 0.47
- Pulled back toward EMA20 0.77 (low 0.74)
- RSI 50 reset, Stoch %K 41 above %D 38 and rising
- ⚠ Loss-making (negative EPS/ROE/net income)

**Fundamentals:** P/E n/a | P/B n/a | EPS -0.15 | ROE -40.4% | Div yield 0.0% | D/E 7.13 | Net income -0.21B | Mkt cap 1.20B

### 2. ADRI - Arab Development & Real Estate Investment (PULLBACK)
Finance | ATR 0.772 (6.4%/day) | ADV 37.5M EGP | RSI 44.6 | EMA10 12.648 | RS vs EGX30 +10.1pts

- Uptrend: EMA20 12.75 > EMA50 11.94 > SMA200 7.94
- Pulled back toward EMA20 12.75 (low 12.10)
- RSI 45 reset, Stoch %K 18 above %D 17 and rising
- ⚠ 1M high 14.7 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield n/a | D/E n/a | Net income n/a | Mkt cap n/a

### 3. AJWA - Ajwa for Food Industries Co. Egypt (PULLBACK)
Consumer Non-Durables | ATR 10.786 (5.1%/day) | ADV 21.6M EGP | RSI 57.9 | EMA10 210.024 | RS vs EGX30 +24.7pts

- Uptrend: EMA20 206.79 > EMA50 196.86 > SMA200 154.13
- Pulled back toward EMA20 206.79 (low 210.02)
- RSI 58 reset, Stoch %K 58 above %D 50 and rising
- ⚠ 1M high 229.98 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield 0.0% | D/E n/a | Net income n/a | Mkt cap 4.29B

## Data quality

Universe 294 | screener OK 238 | recovered from fallback 0 | dropped 56

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALEX: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- APPC: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- BQDC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-11-02)
- DCRC: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- EEP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EFAC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGOTH: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS30AJ1C016-EGP: stale bar 2026-11-02 (session 2026-11-03); fallback history too short
- EGS3E071C013-EGP: screener missing sma200; fallback history too short
- EGS48271C018-EGP: stale bar 2026-11-02 (session 2026-11-03); fallback history too short
- EGS65101C015: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65621C012: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65861C014: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS659O1C015: stale bar 2026-11-02 (session 2026-11-03); fallback history too short
- EGS72L31C011: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGWA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EITP: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- ELAB: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ENPI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GEOS: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GOUR: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- GROV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GTHE: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- HDST: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- IRAX: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- KNGC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- KORA: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- LKGP: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- MITR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MLIC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MMHC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NAMI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBKE: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- NCGC: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- NFCI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NMIN: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- OCAP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- PACH: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- PMSC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- POCO: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- RMTV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SIEG: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SINA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SMPP: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- SNFI: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- SUCE: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- TORA: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- WATP: stale bar 2026-11-02 (session 2026-11-03); fallback fetch failed (HTTP Error 404: Not Found)
- YAYT: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)

<details><summary>Run log</summary>

| Stage | Outcome | Detail |
|---|---|---|
| UNIVERSE | OK | 294 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-11-03 (newest trade in screener data) |
| VALIDATE | PARTIAL | 238 ready, 56 need recovery |
| RECOVER | PARTIAL | 0 recovered, 56 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/5 pullback candidates |
| SCAN | OK | 3 setups from 238 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
