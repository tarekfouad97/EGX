# EGX Swing Scan - session 2026-10-07

_Generated 2026-10-10 15:49 Cairo. Run status: **DEGRADED**._

> ⚠ Some data came from the fallback source or was dropped. See Data quality below.

**Regime: RISK-OFF** | EGX30 53,265 (-6.2% 1M) - EGX30 below 50 EMA with 20 < 50 - risk halved, breakouts suppressed

Scanned 98 stocks, 20 filtered out (currency/liquidity/volatility), **4 setups**. Sizing: 100,000 EGP capital, 1.0% risk/trade x 0.5 regime multiplier.

AI news & fundamentals review: skipped - ANTHROPIC_API_KEY not set.

| # | Ticker | Setup | Q | Close | Entry (buy-stop) | Stop | T1 | T2 | R:R T1 | Risk % | Shares | Position EGP |
|---|--------|-------|---|-------|------------------|------|----|----|--------|--------|--------|--------------|
| 1 | **SUGR** | PULLBACK | 75 | 55.76 | 56.27 | 53.30 | 60.73 | 65.18 | 1.5R | 5.3% | 168 | 9,453 |
| 2 | **ABUK** | PULLBACK | 75 | 90.00 | 90.32 | 83.38 | 100.73 | 111.14 | 1.5R | 7.7% | 72 | 6,503 |
| 3 | **ATQA** | PULLBACK | 75 | 12.25 | 12.36 | 11.40 | 13.80 | 15.24 | 1.5R | 7.8% | 520 | 6,427 |
| 4 | **MOIN** | PULLBACK | 70 | 35.49 | 37.10 | 32.76 | 43.61 | 50.12 | 1.5R | 11.7% | 115 | 4,266 |

### 1. SUGR - Delta Sugar (PULLBACK)
Process Industries | ATR 2.610 (4.7%/day) | ADV 9.4M EGP | RSI 49.3 | EMA10 55.227 | RS vs EGX30 -1.4pts

- Uptrend: EMA20 56.01 > EMA50 54.91 > SMA200 49.53
- Pulled back toward EMA20 56.01 (low 54.61)
- RSI 49 reset, Stoch %K 44 above %D 38 and rising
- ⚠ Loss-making (negative EPS/ROE/net income)

**Fundamentals:** P/E n/a | P/B 3.87 | EPS -9.78 | ROE -42.7% | Div yield 0.0% | D/E 2.27 | Net income -0.53B | Mkt cap 7.93B | Next earnings 2026-12-02

### 2. ABUK - Abou Kir Fertilizers & Chemical Industries Co. (PULLBACK)
Process Industries | ATR 3.154 (3.5%/day) | ADV 65.3M EGP | RSI 55.2 | EMA10 88.494 | RS vs EGX30 +8.4pts

- Uptrend: EMA20 88.37 > EMA50 84.96 > SMA200 74.87
- Pulled back toward EMA20 88.37 (low 86.35)
- RSI 55 reset, Stoch %K 33 above %D 31 and rising
- ⚠ 1M high 96.29 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B 3.53 | EPS n/a | ROE n/a | Div yield 9.2% | D/E n/a | Net income 7.98B | Mkt cap 113.57B | Next earnings 2026-10-28

### 3. ATQA - Misr National Steel (PULLBACK)
Producer Manufacturing | ATR 0.547 (4.5%/day) | ADV 59.3M EGP | RSI 52.9 | EMA10 12.045 | RS vs EGX30 +5.0pts

- Uptrend: EMA20 12.12 > EMA50 11.68 > SMA200 9.98
- Pulled back toward EMA20 12.12 (low 11.90)
- RSI 53 reset, Stoch %K 43 above %D 37 and rising
- ⚠ 1M high 13.7 sits below T1 - resistance

**Fundamentals:** P/E n/a | P/B n/a | EPS n/a | ROE n/a | Div yield 0.0% | D/E n/a | Net income n/a | Mkt cap 14.70B

### 4. MOIN - Mohandes Insurance Co. (PULLBACK)
Finance | ATR 2.422 (6.8%/day) | ADV 11.4M EGP | RSI 50.6 | EMA10 35.265 | RS vs EGX30 -9.4pts

- Uptrend: EMA20 35.47 > EMA50 33.98 > SMA200 26.23
- Pulled back toward EMA20 35.47 (low 34.61)
- RSI 51 reset, Stoch %K 50 above %D 47 and rising

**Fundamentals:** P/E n/a | P/B 6.16 | EPS n/a | ROE n/a | Div yield 0.0% | D/E 0.00 | Net income 0.38B | Mkt cap 9.23B

## Data quality

Universe 100 | screener OK 98 | recovered from fallback 0 | dropped 2

**Dropped** (no fresh, complete data from any source):

- CPME: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)
- GOUR: screener missing sma200; fallback fetch failed (HTTP Error 404: Not Found)

<details><summary>Run log</summary>

| Stage | Outcome | Detail |
|---|---|---|
| UNIVERSE | OK | 100 stocks from TradingView |
| INDEX | OK | EGX30 from TradingView |
| SESSION | OK | 2026-10-07 (newest trade in screener data) |
| VALIDATE | PARTIAL | 98 ready, 2 need recovery |
| RECOVER | PARTIAL | 0 recovered, 2 dropped |
| ENRICH | PARTIAL | previous-bar Stoch for 6/8 pullback candidates |
| SCAN | OK | 4 setups from 98 stocks |
| AI_REVIEW | SKIPPED | ANTHROPIC_API_KEY not set |

</details>

## How to use
- **Entry** is a buy-stop above the session's high: only trigger if price trades through it in the next session. Cancel if not filled within 2 sessions.
- **Stop** is hard. Sell half at **T1** (R:R column; 1.5R, or EMA20 for bounces), move stop to entry, trail the rest to **T2** (3R) or exit on a close below EMA10.
- Time stop: exit after ~10 sessions if neither target nor stop is hit.

_Analytical output only - not licensed financial advice._
