# Backtest 2023-09-26 to 2026-11-02

245 stocks, 751 sessions, 3674 raw signals. Regime days: {'RISK-ON': 490, 'NEUTRAL': 170, 'RISK-OFF': 91}.
All results after Thndr fees, 20,000 EGP account.

| Variant | Trades | Win % | Avg R | Profit factor | Return % | Max DD % | Avg days |
|---|---|---|---|---|---|---|---|
| A_as_emailed | 627 | 42.3 | 0.0 | 1.02 | 2.5 | -25.7 | 7.3 |
| B_no_buys_in_riskoff | 572 | 44.1 | 0.039 | 1.06 | 14.6 | -16.3 | 7.3 |
| C_riskon_only | 366 | 43.4 | -0.023 | 0.95 | -8.4 | -20.9 | 7.3 |
| D_top5_q70 | 398 | 42.2 | -0.035 | 0.89 | -18.8 | -38.8 | 7.4 |
| E_D_plus_t1_1R | 463 | 49.7 | -0.027 | 0.93 | -13.4 | -33.4 | 6.6 |
| F_D_plus_t1_1.25R | 417 | 44.6 | -0.043 | 0.87 | -22.1 | -43.1 | 7.0 |
| G_as_emailed_t1_1R | 666 | 45.9 | -0.049 | 0.91 | -22.7 | -29.9 | 6.7 |
| H_scan_riskon_trail3ATR | 219 | 34.2 | 0.093 | 1.18 | 20.3 | -20.1 | 15.3 |
| I_scan_riskon_belowEMA50 | 141 | 32.6 | 0.28 | 1.54 | 48.2 | -18.8 | 24.1 |
| J_scan_noRiskoff_trail3ATR | 342 | 36.0 | 0.206 | 1.28 | 42.7 | -18.0 | 15.2 |
| K_donch50_trail3ATR | 473 | 40.6 | 0.456 | 1.85 | 192.0 | -15.7 | 11.5 |
| L_donch50_riskon_trail3ATR | 350 | 38.9 | 0.395 | 1.72 | 136.3 | -18.8 | 11.0 |
| M_donch50_belowEMA50 | 193 | 32.1 | 0.645 | 2.05 | 138.6 | -15.8 | 30.6 |
| N_donch50_trail4ATR | 322 | 37.9 | 0.466 | 1.82 | 136.5 | -14.9 | 18.2 |
| O_donch50_riskon_trail3ATR_max6 | 211 | 40.3 | 0.537 | 1.98 | 111.5 | -15.0 | 12.1 |
| P_LIVE_scanner_trend | 479 | 40.1 | 0.399 | 1.75 | 170.4 | -17.3 | 11.4 |
