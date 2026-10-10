# EGX Swing Trader - Requirements

Status: living document. Each requirement has an ID so that code, tests and reviews can refer to it.
"Must" is mandatory, "should" is expected unless there is a documented reason.

## 1. Purpose and scope

The EGX Swing Trader scans the largest stocks on the Egyptian Exchange (EGX) after each session and suggests
long-only swing trades, meant to be held for about 2–10 sessions. Each suggestion comes with an entry, stop, targets
and a position size.

**In scope:** data collection, setup detection, trade planning, position sizing, a daily report, and scheduled
automation.

**Out of scope:** placing or managing orders, short selling, intraday trading, fundamentals and news, and portfolio
tracking of trades that were actually taken.

The output is analytical only and is not financial advice. Every report must say so.

## 2. Users and usage

| User | Need |
|------|------|
| Trader | Reads the daily report after the close and decides which suggestions to act on in the next session. |
| Maintainer | Changes rules or thresholds, and needs tests that fail when a rule breaks. |
| Automation | GitHub Actions runs the scan Sunday to Thursday and commits the report. |

## 3. Functional requirements

### 3.1 Universe and data

| ID | Requirement |
|----|-------------|
| FR-1 | The universe must be the top N (default 100) primary EGX common stocks by market cap. |
| FR-2 | The primary source must be TradingView's Egypt screener on the daily timeframe. |
| FR-3 | The fallback source must be Yahoo Finance daily candles (`<TICKER>.CA`). Indicators are computed locally with TradingView's definitions (EMA seeded with an SMA, Wilder RSI/ATR/ADX, Stoch 14/3/3, MACD 12/26/9, BB 20/2, Perf.1M = close vs the last close before the same day one month earlier). |
| FR-4 | The **session date** must be the date (Cairo time) of the newest trade in the data, not the date the scan ran. |
| FR-5 | A stock's data must be **complete**: every field in `pipeline.REQUIRED` is a finite number. |
| FR-6 | A stock's data must be **fresh**: its last bar is on the session date. |
| FR-7 | Previous-bar Stoch must come from candle history, never from the screener's `Stoch.K[1]` / `Stoch.D[1]`, which were found to be inconsistent with its own %D. |
| FR-8 | Only EGP-quoted stocks are tradeable. USD-quoted listings must be excluded with a reason. |
| FR-9 | Stocks must be excluded when average daily value traded is below the floor (default 5M EGP), or when ATR is outside 1–8% of price. |

### 3.2 Setups (one per stock; priority PULLBACK > BREAKOUT > BOUNCE)

| ID | Setup | Conditions |
|----|-------|------------|
| FR-10 | PULLBACK | EMA20 > EMA50 > SMA200 and close > SMA200; low within 0.5 ATR of EMA20; close between EMA50 and EMA20 + 1 ATR; RSI 38–58; Stoch %K > %D, %K < 60, and %K rising when the previous bar is known. |
| FR-11 | BREAKOUT | close ≥ 99% of the 1-month high; volume ≥ 1.5× the 10-day average; ADX > 20 with +DI > −DI; RSI 55–78; close > EMA50. |
| FR-12 | BOUNCE | close > SMA200; RSI < 35, or RSI rising from below 30; low within 1% of the lower Bollinger band; RSI rising or Stoch %K > %D. |
| FR-13 | Every reason printed for a setup must describe the actual data, for example "crossed above today" versus "above and rising". |

### 3.3 Market regime (EGX30)

| ID | Requirement |
|----|-------------|
| FR-14 | RISK-ON when close > EMA20 > EMA50: risk × 1.0. |
| FR-15 | RISK-OFF when close < EMA50 and EMA20 < EMA50: risk × 0.5, and no breakouts. |
| FR-16 | NEUTRAL for anything else: risk × 0.75. |
| FR-17 | UNKNOWN when EGX30 data is unavailable: risk × 0.5, and no breakouts. |

### 3.4 Trade plan

| ID | Requirement |
|----|-------------|
| FR-18 | The entry is a buy-stop at high + 0.1 ATR. It must be at least one tick above the session high and is rounded **up** to the tick. |
| FR-19 | Ticks come from the stock's price scale: 0.01 EGP, or 0.001 under 1 EGP. Stops round **down**, and targets round to the nearest tick. |
| FR-20 | Stops: PULLBACK min(low, EMA50) − 0.5 ATR; BREAKOUT entry − 1.5 ATR; BOUNCE low − 0.75 ATR. |
| FR-21 | Targets: T1 = 1.5R and T2 = 3R. BOUNCE T1 = EMA20, kept between 1R and 1.5R. |
| FR-22 | Shares = (capital × risk% × regime multiplier) / R. The position is capped at 25% of capital and at 10% of average daily value traded. |
| FR-23 | Ranking = setup quality ± relative strength vs EGX30 (±10 beyond ±3 points) − 5 per warning. Sizing caps are notes and must not affect the ranking. |
| FR-24 | Warnings: resistance (1-month or 52-week high) between the entry and T1, and a 1-month gain above 25%. |

### 3.5 Outputs

| ID | Requirement |
|----|-------------|
| FR-25 | A markdown report containing: session date, run status, regime, a signals table (with R:R), per-stock reasons, warnings and notes, a **Data quality** section and how-to-use rules. |
| FR-26 | `--out-dir` writes `<session>.md`, `<session>.json` and `latest.md`, all UTF-8. A run with no known session writes `<run-date>-FAILED.*` so it never overwrites a good report. |
| FR-27 | The JSON contains signals, exclusions, `data_status` per stock, `events` (the run log), `run_status`, `as_of` and `intraday`. |
| FR-28 | A run during an open session (before 14:45 Cairo on the session date) must be flagged `intraday`. |
| FR-29 | `--input` replays a saved snapshot offline and must refuse `--out-dir`. |

## 4. Error handling: always produce a report

**Hard requirement (EH-0): every run that starts must end with a report on disk and exit code 0.**
Data problems lower the run status. They never stop the run.

### 4.1 Run state machine

```mermaid
stateDiagram-v2
    [*] --> UNIVERSE
    UNIVERSE --> INDEX: screener OK (cache refreshed)
    UNIVERSE --> INDEX: screener failed -> cached universe (all to recovery)
    UNIVERSE --> INDEX: no cache -> empty universe
    INDEX --> SESSION: TradingView EGX30 OK
    INDEX --> SESSION: failed -> EGX30 from candles
    INDEX --> SESSION: failed -> UNKNOWN regime
    SESSION --> VALIDATE
    VALIDATE --> RECOVER: stocks missing fields or stale
    VALIDATE --> ENRICH: all stocks ready
    RECOVER --> ENRICH
    ENRICH --> SCAN
    SCAN --> REPORT: signals
    SCAN --> REPORT: scan error -> zero signals, logged
    REPORT --> [*]
```

| ID | Stage | Primary | Fallback chain | On total failure |
|----|-------|---------|----------------|------------------|
| EH-1 | UNIVERSE | TradingView, 3 attempts with backoff (2s, 4s) | cached `data/universe.json` (written on every successful fetch) | empty universe, status FAILED |
| EH-2 | INDEX | TradingView EGX30, 3 attempts | EGX30 computed from Yahoo candles | regime UNKNOWN (FR-17) |
| EH-3 | SESSION | newest trade date in screener data | EGX30 bar date, then newest recovered bar | "unknown" session |
| EH-4 | VALIDATE | each stock checked against FR-5 and FR-6 | stocks that fail move to RECOVER | - |
| EH-5 | RECOVER | Yahoo candles, 2 attempts, computed with FR-3 | - | stock DROPPED, with the reason |
| EH-6 | ENRICH | previous-bar Stoch from candles for PULLBACK candidates | - | Stoch prev stays unknown; the "rising" check is skipped and the reason says "above %D" |
| EH-7 | SCAN | `setups.scan` | - | zero signals, error logged |
| EH-8 | CLI | the whole pipeline | - | emergency report, status FAILED, with the exception in the run log |
| EH-9 | Workflow | unit tests | a test failure is flagged in the job summary and never blocks the scan | the scan and commit steps run `if: always()` |

### 4.2 Per-stock state machine

```mermaid
stateDiagram-v2
    [*] --> CHECK
    CHECK --> READY: complete and fresh (screener)
    CHECK --> NEEDS_RECOVERY: missing fields / stale bar / no screener data
    NEEDS_RECOVERY --> RECOVERED: fallback fetched, history >= 210 bars, last bar = session, complete
    NEEDS_RECOVERY --> DROPPED: fetch failed / history too short / fallback stale / still incomplete
    READY --> [*]
    RECOVERED --> [*]
    DROPPED --> [*]
```

| ID | Requirement |
|----|-------------|
| EH-10 | Data from the two sources must not be mixed for one stock. A recovered stock uses fallback indicators for every field, and keeps only its metadata (symbol, name, sector, currency, price scale) from the screener or cache. |
| EH-11 | A stock with no fresh data from any source must be dropped and listed in the report with the reason. Old data must never be used. |

### 4.3 Run status

| Status | Meaning |
|--------|---------|
| OK | All stages succeeded on primary data, and nothing was dropped. |
| DEGRADED | At least one fallback was used, or at least one stock was dropped. The report is still usable. |
| FAILED | No tradeable stocks, or an unexpected error. The report says **no trades**. |
| OFFLINE | Replay of a saved snapshot (`--input`). |

## 5. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-1 | Python 3.9+, standard library only. Must run without `tzdata` by falling back to built-in Egypt DST rules. |
| NFR-2 | A normal run should take under 60 seconds. A full-fallback run (screener down) of 100 stocks should take under 2 minutes, using 8 parallel requests. |
| NFR-3 | Network calls have timeouts (20–30 seconds) and bounded retries. Nothing may hang the workflow. |
| NFR-4 | Workflow inputs reach the shell only through environment variables, never through `${{ }}` inside `run:`. |
| NFR-5 | Unit tests must cover every setup condition, so that removing any one condition fails a test (checked by mutation runs), and every fallback path in sections 4.1 and 4.2. |
| NFR-6 | Reports are deterministic for the same input data. |

## 6. Schedule and automation

| ID | Requirement |
|----|-------------|
| AU-1 | Runs Sunday to Thursday at 13:00 UTC, which is after the 14:30 Cairo close in both summer and winter time. |
| AU-2 | Can be started by hand with capital and risk % inputs. |
| AU-3 | Commits `reports/` and `data/universe.json`. Checks out the branch tip and rebases before pushing, so that runs queued one after another don't conflict. |

## 7. Known limitations

- Yahoo has no usable EGX30 history, so when TradingView is down the regime is UNKNOWN. Risk is halved and breakouts
  are skipped.
- Fallback indicators can differ slightly from TradingView's. Measured on 8 large caps: about 0.1% for moving
  averages, about 0.2 points for RSI and about 2% for ADX and ATR. Yahoo can also have gaps in thinly traded names.
- Newly listed stocks with fewer than 210 sessions of history cannot be scored and are dropped.
- The rules have not been backtested, so the win rate is unknown.
