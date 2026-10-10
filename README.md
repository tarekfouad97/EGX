# EGX Swing Trader

A scanner for long-only swing trades on the Egyptian Exchange, aimed at holds of about 2–10 sessions. Each day it pulls
indicator data for the largest EGX stocks from TradingView's Egypt screener. It drops names that are illiquid or
too quiet or too volatile to swing. It then finds setups and gives an entry, stop, targets and position size for
each one. It only suggests trades. It never places orders.

The scanner itself uses only the Python standard library (3.9+). The optional AI review needs the `anthropic`
package (`pip install -r requirements.txt`). On Windows without the `tzdata`
package it falls back to built-in Egypt DST rules.

Full requirements, including the error-handling state machine, are in
[docs/REQUIREMENTS.md](docs/REQUIREMENTS.md).

## Always a report

A run never stops on bad data, and every run ends with a report on disk.

- If a stock's TradingView data is missing or stale, the scanner fetches its daily candles from Yahoo Finance and
  computes the indicators itself.
- If that data isn't fresh for the session either, the stock is **dropped**, and the report lists it with the reason.
- If TradingView is down entirely, the universe comes from `data/universe.json`, which is refreshed on every
  successful run. Every stock then goes through the Yahoo fallback.

Each report carries a run status:

| Status | Meaning |
|--------|---------|
| OK | All data came from TradingView and nothing was dropped. |
| DEGRADED | A fallback was used, or some stocks were dropped. The report is still usable. |
| FAILED | No usable data. The report says no trades. |

The **Data quality** section lists recovered and dropped stocks and the full run log.

## Fundamentals and news review (AI)

Picks come only from the chart setups. A second layer then checks each pick before it reaches the report:

- **Fundamentals** (from TradingView): P/E, P/B, EPS, ROE, dividend yield, D/E, net income, market cap and the next
  earnings date are shown under each pick. Two rules apply without any AI. A loss-making company gets a warning, and
  so does an earnings release inside the holding window (16 days). Each warning lowers the rank.
- **AI review** (Claude, with web search): Claude checks company news from the last 60 days, upcoming corporate
  actions (earnings, dividends, rights issues, suspensions, deals) and the fundamentals. It returns a verdict:
  - **CONFIRM:** no change.
  - **CAUTION:** a warning and a lower rank.
  - **AVOID:** the pick moves to a "Vetoed - do not trade" section.

  The headlines it used are linked in the report. The AI can only demote or veto a pick, never add one or raise its
  rank.

The in-workflow AI review is optional. The `egx-swing-review` skill (below) does the same job in your Claude chat
without an API key. **To turn on the in-workflow review as well**, add a repository secret named `ANTHROPIC_API_KEY` (Settings → Secrets and variables →
Actions). Without it the review is skipped and the report says so; everything else still runs. Locally, run
`pip install -r requirements.txt` and export the key. Use `--no-ai` to skip the review, or `--ai-max N` to cap how many
picks are reviewed (default 8). Cost scales with the number of picks: at most 5 web searches per pick, and nothing on
days with no setups.

## Final answer in chat: the `egx-swing-review` skill

The recommended way to use the AI review is the Claude Code skill in `.claude/skills/egx-swing-review/`. In Claude
Code, opened on this repo, run:

```
/egx-swing-review                 # defaults: 100,000 EGP, 1% risk per trade
/egx-swing-review 250000 0.5
```

or just ask "give me today's EGX swing picks". The skill:

1. triggers the GitHub workflow with your capital and risk,
2. waits for it to finish,
3. reads `reports/latest.json`,
4. researches news, corporate actions and fundamentals for every pick,
5. answers in chat with a final table: **TAKE / TAKE SMALLER / SKIP**, with entry, stop, targets, shares and linked
   headlines.

Like the in-workflow review, it can only demote or veto a pick. It needs no API key: the research runs in your Claude
session. It triggers the workflow with the `gh` CLI or the GitHub connector; with neither, it runs the scanner
locally.

## Email

Every workflow run emails the report: a plain "what to buy" table, money used, the most you could lose, the
best-case profit and the warnings, with the full report attached. It goes to `tare2fo2ad@gmail.com` (set in the
workflow; a `MAIL_TO` repository secret overrides it, comma-separated for several people).

To turn it on, add two repository secrets (Settings → Secrets and variables → Actions → New repository secret):

| Secret | Value |
|--------|-------|
| `SMTP_USERNAME` | the Gmail address that sends the email |
| `SMTP_PASSWORD` | a Gmail **App Password** (Google Account → Security → 2-Step Verification → App passwords), not your normal password |

Without them the email step is skipped; a failed email never fails the run. Other providers work too, via the
`SMTP_HOST` / `SMTP_PORT` environment variables (SSL, default `smtp.gmail.com:465`). The email contains the scanner's
picks; the news-checked TAKE / TAKE SMALLER / SKIP answer comes from the `/egx-swing-review` skill.

## Run it on demand

```bash
python -m egx_swing                                  # markdown report to stdout
python -m egx_swing --capital 250000 --risk-pct 0.75
python -m egx_swing --top 150 --min-adv 2000000      # wider universe, lower liquidity floor
python -m egx_swing --out-dir reports                # also write reports/<session-date>.md, .json, latest.md
python -m egx_swing --json                           # machine-readable output
python -m egx_swing --no-ai                          # skip the Claude news & fundamentals review
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

1. runs the unit tests (a failure is flagged in the summary, but never blocks the report),
2. runs the scan and writes the report to the job summary,
3. commits `reports/<session-date>.md`, `reports/<session-date>.json`, `reports/latest.md`,
   `reports/latest.json` and `data/universe.json`.

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
| UNKNOWN | EGX30 data unavailable | 50% risk and no breakouts |

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
