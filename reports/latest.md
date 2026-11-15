# EGX Swing Scan - session 2026-11-15

_Generated 2026-11-15 21:13 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: NEUTRAL** | EGX30 52,187 (+1.3% 1M) - EGX30 mixed vs 20/50 EMAs - risk reduced to 75%

Scanned 238 stocks, 76 filtered out (currency/liquidity/volatility), **5 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.75 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **ATLC** | BREAKOUT | 80 | 5.94 | 6.00 | 5.37 | 6.94 | 7.89 | 1.5R | 10.5% | 238 | 1,428 |
| 2 | **MICH** | BREAKOUT | 75 | 48.57 | 49.06 | 45.76 | 54.01 | 58.96 | 1.5R | 6.7% | 45 | 2,208 |
| 3 | **SCEM** | BREAKOUT | 65 | 103.90 | 104.92 | 98.12 | 115.12 | 125.32 | 1.5R | 6.5% | 22 | 2,308 |
| 4 | **ORAS** | PULLBACK | 55 | 827.02 | 829.87 | 785.67 | 896.17 | 962.47 | 1.5R | 5.3% | 3 | 2,490 |
| 5 | **AMOC** | PULLBACK | 55 | 13.67 | 13.75 | 12.69 | 15.34 | 16.93 | 1.5R | 7.7% | 141 | 1,939 |

### 1. ATLC - Al Tawfeek Leasing Company-A.T.LEASE (BREAKOUT)
Finance | ATR 0.410 (6.9%/day) | ADV 17.2M EGP | RSI 61.4 | EMA10 5.289 | RS vs EGX30 +5.5pts

- Close 5.94 at 1M high 5.95
- Volume 1.7x 10d avg
- ADX 25 with +DI 25 > -DI 19, RSI 61

**Fundamentals:** P/E n/a | P/B 1.66 | EPS n/a | ROE n/a | Div yield 6.2% | D/E 5.30 | Net income 0.23B | Mkt cap 2.38B

### 2. MICH - Misr Chemical Industries Ltd. (BREAKOUT)
Process Industries | ATR 2.196 (4.5%/day) | ADV 10.7M EGP | RSI 68.1 | EMA10 44.302 | RS vs EGX30 +14.5pts

- Close 48.57 at 1M high 48.84
- Volume 1.8x 10d avg
- ADX 24 with +DI 32 > -DI 18, RSI 68
- ⚠ 52W high 53.9 sits below T1 - resistance

**Fundamentals:** P/E 9.89 | P/B 3.38 | EPS 4.91 | ROE n/a | Div yield 7.0% | D/E 0.13 | Net income 0.57B | Mkt cap 5.33B | Next earnings 2026-12-02

### 3. SCEM - Sinai Cement Co. (BREAKOUT)
Non-Energy Minerals | ATR 4.524 (4.4%/day) | ADV 64.2M EGP | RSI 71.8 | EMA10 96.033 | RS vs EGX30 +18.6pts

- Close 103.90 at 1M high 104.46
- Volume 2.6x 10d avg
- ADX 22 with +DI 34 > -DI 14, RSI 72
- ⚠ 52W high 113 sits below T1 - resistance

**Fundamentals:** P/E 8.78 | P/B 4.50 | EPS 11.84 | ROE 51.3% | Div yield 0.0% | D/E 0.02 | Net income 2.28B | Mkt cap 27.10B

### 4. ORAS - Orascom Construction Plc (PULLBACK)
Industrial Services | ATR 28.445 (3.4%/day) | ADV 181.5M EGP | RSI 52.2 | EMA10 809.596 | RS vs EGX30 -10.1pts

- Uptrend: EMA20 815.00 > EMA50 814.54 > SMA200 672.62
- Pulled back toward EMA20 815.00 (low 799.90)
- RSI 52 reset, Stoch %K 57 above %D 48 and rising
- ⚠ 1M high 895 sits below T1 - resistance

**Fundamentals:** P/E 8.01 | P/B 2.15 | EPS 103.27 | ROE 26.6% | Div yield 3.2% | D/E 0.54 | Net income 9.46B | Mkt cap 98.54B

### 5. AMOC - Alexandria Mineral Oils Co. (PULLBACK)
Energy Minerals | ATR 0.563 (4.1%/day) | ADV 144.7M EGP | RSI 54.8 | EMA10 13.321 | RS vs EGX30 -0.5pts

- Uptrend: EMA20 13.36 > EMA50 12.98 > SMA200 9.71
- Pulled back toward EMA20 13.36 (low 13.04)
- RSI 55 reset, Stoch %K 26 above %D 21 and rising
- ⚠ 1M high 15.15 sits below T1 - resistance

**Fundamentals:** P/E 12.06 | P/B 3.30 | EPS 1.13 | ROE 33.7% | Div yield 9.2% | D/E 0.00 | Net income 1.33B | Mkt cap 17.65B | Next earnings 2026-12-02

## Data quality

Universe 294 | screener OK 238 | recovered from fallback 0 | dropped 56

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALEX: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- APPC: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- APPF: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- BQDC: screener missing adx; fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-11-12)
- DCRC: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- EEP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EFAC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGOTH: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS30AJ1C016-EGP: stale bar 2026-11-11 (session 2026-11-15); fallback history too short
- EGS3E071C013-EGP: screener missing sma200; fallback history too short
- EGS48271C018-EGP: stale bar 2026-11-11 (session 2026-11-15); fallback history too short
- EGS65101C015: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65621C012: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS65861C014: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGS659O1C015: stale bar 2026-11-11 (session 2026-11-15); fallback history too short
- EGS72L31C011: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EGWA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- EITP: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- ELAB: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ENPI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GEOS: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GOUR: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- GROV: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- GTHE: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- HDST: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- IRAX: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- KNGC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- KORA: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- LKGP: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- MITR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MLIC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- MMHC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NAMI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NBKE: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- NCGC: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- NFCI: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- NMIN: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- OCAP: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- PACH: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- PMSC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- POCO: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SIEG: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SINA: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- SMPP: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- SNFI: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- SUCE: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- TORA: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- WATP: stale bar 2026-11-11 (session 2026-11-15); fallback fetch failed (HTTP Error 404: Not Found)
- YAYT: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)

<details><summary>Run log</summary>

| Stage | Outcome | Detail |
|---|---|---|
| UNIVERSE | OK | 294 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-11-15 (newest trade in screener data) |
| VALIDATE | PARTIAL | 238 ready, 56 need recovery |
| RECOVER | PARTIAL | 0 recovered, 56 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/2 pullback candidates |
| SCAN | OK | 5 setups from 238 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
