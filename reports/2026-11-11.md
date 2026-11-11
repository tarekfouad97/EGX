# EGX Swing Scan - session 2026-11-11

_Generated 2026-11-11 21:59 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: NEUTRAL** | EGX30 52,500 (+0.6% 1M) - EGX30 mixed vs 20/50 EMAs - risk reduced to 75%

Scanned 256 stocks, 99 filtered out (currency/liquidity/volatility), **3 setups**. Sizing: 20,000 EGP capital, 1.0% risk/trade x 0.75 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **CANA** | BREAKOUT | 85 | 51.02 | 51.71 | 48.41 | 56.66 | 61.61 | 1.5R | 6.4% | 45 | 2,327 |
| 2 | **EAST** | BREAKOUT | 65 | 35.00 | 35.33 | 33.42 | 38.19 | 41.06 | 1.5R | 5.4% | 78 | 2,756 |
| 3 | **BINV** | PULLBACK | 65 | 55.50 | 57.12 | 52.70 | 63.75 | 70.38 | 1.5R | 7.7% | 33 | 1,885 |

### 1. CANA - Suez Canal Bank SAE (BREAKOUT)
Finance | ATR 2.199 (4.3%/day) | ADV 25.7M EGP | RSI 67.3 | EMA10 47.433 | RS vs EGX30 +18.0pts

- Close 51.02 at 1M high 51.49
- Volume 2.9x 10d avg
- ADX 27 with +DI 34 > -DI 13, RSI 67
- ⚠ 52W high 52 sits below T1 - resistance

**Fundamentals:** P/E 8.32 | P/B 2.52 | EPS 6.13 | ROE 30.9% | Div yield 0.0% | D/E 1.68 | Net income 5.65B | Mkt cap 51.02B | Next earnings 2026-12-02

### 2. EAST - Eastern Company (BREAKOUT)
Consumer Non-Durables | ATR 1.265 (3.6%/day) | ADV 30.0M EGP | RSI 67.1 | EMA10 32.900 | RS vs EGX30 +23.9pts

- Close 35.00 at 1M high 35.20
- Volume 2.2x 10d avg
- ADX 22 with +DI 28 > -DI 18, RSI 67
- ⚠ Earnings due 2026-11-18 - inside the holding window

**Fundamentals:** P/E 11.83 | P/B 6.29 | EPS 2.96 | ROE 62.3% | Div yield 12.8% | D/E 0.55 | Net income 8.66B | Mkt cap 105.00B | Next earnings 2026-11-18

### 3. BINV - B Investments Holding SAE (PULLBACK)
Finance | ATR 2.609 (4.7%/day) | ADV 8.8M EGP | RSI 53.2 | EMA10 54.009 | RS vs EGX30 -4.9pts

- Uptrend: EMA20 54.52 > EMA50 54.38 > SMA200 46.62
- Pulled back toward EMA20 54.52 (low 54.01)
- RSI 53 reset, Stoch %K 48 above %D 35 and rising
- ⚠ 1M high 62.5 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B 2.07 | EPS n/a | ROE n/a | Div yield 2.8% | D/E 0.00 | Net income 0.57B | Mkt cap 12.12B | Next earnings 2026-12-02

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
- DCCC: screener missing atr, vol_avg_10d, ema20, ema50 ...; fallback also stale (last bar 2026-11-10)
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
| SESSION | OK | 2026-11-11 (newest trade in screener data) |
| VALIDATE | PARTIAL | 256 ready, 39 need recovery |
| RECOVER | PARTIAL | 0 recovered, 39 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 0/5 pullback candidates |
| SCAN | OK | 3 setups from 256 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
