# EGX Swing Trader

A scanner for long-only swing trades on the Egyptian Exchange, aimed at holds of about 2–10 sessions. Each day it pulls
indicator data for the largest EGX stocks from TradingView's Egypt screener. It drops names that are illiquid or
too quiet or too volatile to swing. It then finds setups and gives an entry, stop, targets and position size for
each one. It only suggests trades. It never places orders.

It uses only the Python standard library (3.9+), so there is nothing to install. On Windows without the `tzdata`
package it falls back to built-in Egypt DST rules.

## Run it on demand

```bash
python -m egx_swing                                  # markdown report to stdout
python -m egx_swing --capital 250000 --risk-pct 0.75
python -m egx_swing --top 150 --min-adv 2000000      # wider universe, lower liquidity floor
python -m egx_swing --out-dir reports                # also write reports/<session-date>.md, .json, latest.md
python -m egx_swing --json                           # machine-readable output
```

Run it after the 14:30 Cairo close. If you run it while the session is still open, the report warns that today's bar
is not final, and the JSON carries `"intraday": true`.

Reports are named after the **session the data is from** (the date of the last trade), not the day you ran it. A
weekend or holiday run therefore updates the previous session's report instead of inventing a new date.
`--input` (offline replay of a saved snapshot) can't be combined with `--out-dir`, so a replay never overwrites
live reports.

## Daily automatic run

`.github/workflows/swing-scan.yml` runs Sunday to Thursday at 13:00 UTC, which is after the close in both summer and
winter time. Each run:

1. runs the unit tests,
2. runs the scan and writes the report to the job summary,
3. commits `reports/<session-date>.md`, `reports/<session-date>.json` and `reports/latest.md`.

You can also start it by hand from the **Actions** tab ("Run workflow") with your own capital and risk %.

## Setups

| Setup | Conditions | Stop |
|-------|------------|------|
| **PULLBACK** | EMA20 > EMA50 > SMA200, low within 0.5 ATR of EMA20, close between EMA50 and EMA20 + 1 ATR, RSI 38–58, Stoch %K above %D, below 60 and rising | below min(low, EMA50) − 0.5 ATR |
| **BREAKOUT** | close ≥ 99% of 1-month high, volume ≥ 1.5× 10-day average, ADX > 20 with +DI > −DI, RSI 55–78 | entry − 1.5 ATR |
| **BOUNCE** | above SMA200, RSI < 35 or turning up from < 30, low within 1% of the lower Bollinger band, RSI rising or Stoch %K > %D | low − 0.75 ATR |

**Universe filter:** EGP-quoted stocks only (the few USD-quoted EGX listings are skipped, since sizing is in EGP),
average daily value traded ≥ 5M EGP, and daily ATR between 1% and 8% of price.

**Market regime (EGX30):**

| Regime | Condition | Effect |
|--------|-----------|--------|
| RISK-ON | close > EMA20 > EMA50 | full risk |
| NEUTRAL | anything else | 75% risk |
| RISK-OFF | close and EMA20 both below EMA50 | 50% risk and no breakouts |

**Trade plan:**

- **Entry:** buy-stop at today's high + 0.1 ATR (at least one tick above the high).
- **Price grid:** levels are rounded to the stock's tick: 0.01 EGP, or 0.001 for stocks under 1 EGP. Entries round
  up and stops round down.
- **Targets:** T1 = 1.5R and T2 = 3R, where R = entry − stop. A BOUNCE uses EMA20 as T1, kept between 1R and 1.5R.
  The report's R:R column shows each T1.
- **Size:** risk = capital × risk% × regime multiplier. A position is capped at 25% of capital and at 10% of one
  day's average value traded.
- **Ranking:** a quality score combines setup strength and relative strength vs EGX30. Each warning lowers it by 5,
  such as resistance (the 1-month or 52-week high) below T1 or being extended after a large 1-month gain. A sizing cap
  is shown as a note and does not affect the ranking.

## Tests

```bash
python -m unittest -v
```

_Analytical output only. This is not licensed financial advice._
