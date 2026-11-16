# EGX Swing Scan - session 2026-11-16

_Generated 2026-11-17 00:43 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: NEUTRAL** | EGX30 52,200 (+1.4% 1M) - EGX30 mixed vs 20/50 EMAs - risk reduced to 75%

Scanned 256 stocks, 102 filtered out (currency/liquidity/volatility), **3 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.75 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **EMFD** | BREAKOUT | 85 | 12.80 | 12.90 | 12.24 | 13.89 | 14.88 | 1.5R | 5.1% | 227 | 2,928 |
| 2 | **ORAS** | PULLBACK | 55 | 815.38 | 841.85 | 796.92 | 909.25 | 976.64 | 1.5R | 5.3% | 3 | 2,526 |
| 3 | **AMOC** | PULLBACK | 50 | 13.36 | 13.83 | 12.71 | 15.51 | 17.19 | 1.5R | 8.1% | 133 | 1,839 |

### 1. EMFD - Emaar Misr for Development SAE (BREAKOUT)
Finance | ATR 0.429 (3.4%/day) | ADV 97.5M EGP | RSI 60.2 | EMA10 12.474 | RS vs EGX30 +5.6pts

- Close 12.80 at 1M high 12.85
- Volume 2.6x 10d avg
- ADX 20 with +DI 18 > -DI 17, RSI 60
- ⚠ Earnings due 2026-12-02 - inside the holding window

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield 0.0% | D/E n/a | Net income n/a | Mkt cap 69.72B | Next earnings 2026-12-02

### 2. ORAS - Orascom Construction Plc (PULLBACK)
Industrial Services | ATR 28.403 (3.5%/day) | ADV 169.2M EGP | RSI 49.5 | EMA10 810.647 | RS vs EGX30 -11.5pts

- Uptrend: EMA20 815.04 > EMA50 814.57 > SMA200 674.67
- Pulled back toward EMA20 815.04 (low 811.13)
- RSI 49 reset, Stoch %K 60 above %D 54 and rising
- ⚠ 1M high 895 sits below T1 - resistance

**Fundamentals:** P/E 7.90 | P/B 2.12 | EPS 103.27 | ROE 26.6% | Div yield 3.2% | D/E 0.54 | Net income 9.46B | Mkt cap 97.15B

### 3. AMOC - Alexandria Mineral Oils Co. (PULLBACK)
Energy Minerals | ATR 0.553 (4.1%/day) | ADV 128.9M EGP | RSI 50.3 | EMA10 13.328 | RS vs EGX30 -2.8pts

- Uptrend: EMA20 13.36 > EMA50 13.00 > SMA200 9.74
- Pulled back toward EMA20 13.36 (low 13.35)
- RSI 50 reset, Stoch %K 25 above %D 23 and rising
- ⚠ 1M high 15.15 sits below T1 - resistance
- ⚠ Earnings due 2026-12-02 - inside the holding window

**Fundamentals:** P/E 11.79 | P/B 3.22 | EPS 1.13 | ROE 33.7% | Div yield 9.2% | D/E 0.00 | Net income 1.33B | Mkt cap 17.25B | Next earnings 2026-12-02

## Data quality

Universe 295 | screener OK 256 | recovered from fallback 0 | dropped 39

**Dropped** (no fresh, complete data from any source):

- ACFR: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ALXD: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- ANCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- APPF: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- BQDC: screener missing adx; fallback fetch failed (HTTP Error 404: Not Found)
- CID: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback fetch failed (HTTP Error 404: Not Found)
- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-11-12)
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
| UNIVERSE | OK | 295 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-11-16 (newest trade in screener data) |
| VALIDATE | PARTIAL | 256 ready, 39 need recovery |
| RECOVER | PARTIAL | 0 recovered, 39 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/4 pullback candidates |
| SCAN | OK | 3 setups from 256 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
