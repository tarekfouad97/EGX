"""Robustness checks for the Donchian trend variant (penny stocks, liquidity, nearby settings). Run: python -m backtest.robustness"""
import json,csv,sys
from datetime import date
from pathlib import Path
sys.path.insert(0,'.')
from backtest.run import load, BASE, TREND
from backtest.engine import daily_rows, donchian_signals, index_rows, simulate, metrics
hist=Path('data/history'); idx=load(hist/'EGX30.csv'); rows={}; bars={}
for p in sorted(hist.glob('*.csv')):
    if p.stem=='EGX30': continue
    c=load(p); r=daily_rows(p.stem,c)
    if r: rows[p.stem]=r; bars[p.stem]={date.fromisoformat(x['date']):(x['open'],x['high'],x['low'],x['close']) for x in c}
ir=index_rows(idx); cfg={'capital':20000.0,'risk_pct':1.0}
start=date(2023,9,26)
def run(label,n=50,stop_atr=2.0,trail=3.0,minpx=0,minadv=None,excl=(),gate='as_is',maxpos=99):
    c2=dict(cfg); 
    if minadv: c2['min_adv_egp']=minadv
    ds=donchian_signals({k:v for k,v in rows.items() if k not in excl},ir,c2,n=n,stop_atr=stop_atr)
    ds={d:(reg,[s for s in sg if s['entry']>=minpx]) for d,(reg,sg) in ds.items() if d>=start}
    v={**BASE,**TREND,'trail_atr':trail,'gate':gate,'max_positions':maxpos,'_aux':rows}
    t,cu=simulate(ds,bars,v); m=metrics(t,cu,20000)
    print(f"{label:34s} trades {m['trades']:4d} win {m['win_rate_pct']:5.1f} PF {m['profit_factor']} ret {m['total_return_pct']:6.1f}% DD {m['max_drawdown_pct']}%")
run('K base (n50, stop2ATR, trail3)')
run('K price>=1 EGP',minpx=1)
run('K price>=1, ADV>=10M',minpx=1,minadv=10e6)
run('K without CRST',excl=('CRST',))
run('K n=20',n=20); run('K n=100',n=100)
run('K trail 2.5',trail=2.5); run('K trail 3.5',trail=3.5)
run('K stop 1.5ATR',stop_atr=1.5); run('K stop 3ATR',stop_atr=3.0)
run('K price>=1, no buys RISK-OFF',minpx=1,gate='no_buy_riskoff')
run('K price>=1, max 6 positions',minpx=1,maxpos=6)
