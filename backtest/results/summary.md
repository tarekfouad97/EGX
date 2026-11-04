# Backtest 2023-09-26 to 2026-11-02

245 stocks, 751 sessions, 6068 raw signals. Regime days: {'RISK-ON': 490, 'NEUTRAL': 170, 'RISK-OFF': 91}.
All results after Thndr fees, 20,000 EGP account.

| Variant | Trades | Win % | Avg R | Profit factor | Return % | Max DD % | Avg days |
|---|---|---|---|---|---|---|---|
| A_as_emailed | 647 | 41.1 | -0.018 | 0.98 | -8.1 | -26.2 | 7.5 |
| B_no_buys_in_riskoff | 553 | 45.0 | 0.054 | 1.12 | 24.3 | -19.0 | 7.7 |
| C_riskon_only | 417 | 48.0 | 0.073 | 1.18 | 29.8 | -14.7 | 7.4 |
| D_top5_q70 | 394 | 40.9 | -0.069 | 0.81 | -31.4 | -38.8 | 7.4 |
| E_D_plus_t1_1R | 468 | 49.8 | -0.02 | 0.95 | -9.8 | -33.4 | 6.5 |
| F_D_plus_t1_1.25R | 412 | 44.4 | -0.036 | 0.9 | -18.1 | -42.9 | 7.0 |
| G_as_emailed_t1_1R | 647 | 46.4 | -0.048 | 0.92 | -20.6 | -29.3 | 7.0 |
| H_scan_riskon_trail3ATR | 253 | 39.5 | 0.271 | 1.59 | 68.0 | -14.0 | 16.3 |
| I_scan_riskon_belowEMA50 | 158 | 31.6 | 0.355 | 1.69 | 56.1 | -19.0 | 23.7 |
| J_scan_noRiskoff_trail3ATR | 353 | 38.0 | 0.28 | 1.48 | 72.7 | -15.8 | 15.8 |
| K_donch50_trail3ATR | 473 | 40.6 | 0.456 | 1.85 | 192.0 | -15.7 | 11.5 |
| L_donch50_riskon_trail3ATR | 350 | 38.9 | 0.395 | 1.72 | 136.3 | -18.8 | 11.0 |
| M_donch50_belowEMA50 | 193 | 32.1 | 0.645 | 2.05 | 138.6 | -15.8 | 30.6 |
| N_donch50_trail4ATR | 322 | 37.9 | 0.466 | 1.82 | 136.5 | -14.9 | 18.2 |
| O_donch50_riskon_trail3ATR_max6 | 211 | 40.3 | 0.537 | 1.98 | 111.5 | -15.0 | 12.1 |
