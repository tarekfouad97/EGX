"""Telegram messages for the morning picks (Bot API, standard library only).

    python -m egx_swing.telegram reports/latest.json        # send the morning picks

Credentials: TELEGRAM_TOKEN and TELEGRAM_CHAT_ID from the environment (GitHub secrets),
or from ~/.egx_telegram (KEY=value lines) on your own machine. Never commit them.

One header message (market, money used, how-to), then one message per pick with
Bought / Watch / Skip buttons. The buttons carry `act:SYMBOL:SESSION`; the bot service
that answers them is a later step, so until then a tap shows nothing.
"""

import argparse
import html
import json
import os
import urllib.parse
import urllib.request

API = "https://api.telegram.org/bot{token}/{method}"


def credentials(env=None):
    env = os.environ if env is None else env
    tok, chat = env.get("TELEGRAM_TOKEN"), env.get("TELEGRAM_CHAT_ID")
    path = os.path.expanduser("~/.egx_telegram")
    if (not tok or not chat) and os.path.exists(path):
        cfg = dict(l.strip().split("=", 1) for l in open(path) if "=" in l)
        tok, chat = tok or cfg.get("TELEGRAM_TOKEN"), chat or cfg.get("TELEGRAM_CHAT_ID")
    return tok, chat


def _p(v, d=2):
    return f"{v:,.{d}f}" if isinstance(v, (int, float)) else "?"


def header(report, sample_note=None):
    e = html.escape
    reg = report.get("regime") or {}
    sig = report.get("signals") or []
    cap = (report.get("config") or {}).get("capital")
    lines = []
    if sample_note:
        lines += [f"🧪 <b>{e(sample_note)}</b>", ""]
    lines.append(f"☀️ <b>EGX picks</b> · data from session {e(str(report.get('as_of') or report.get('date', '?')))}")
    if report.get("intraday"):
        lines.append("⚠️ Session was still open - levels are not final.")
    lines.append(f"Market: <b>{e(reg.get('regime', '?'))}</b>" +
                 (" (sizes halved)" if reg.get("risk_mult", 1) < 1 else ""))
    if report.get("run_status") == "FAILED":
        lines += ["", "No usable market data - no trades today."]
    elif not sig:
        lines += ["", "No new buys today. Cash is a position."]
    else:
        money = sum(s["shares"] * s["entry"] for s in sig)
        loss = sum(s["shares"] * (s["entry"] - s["stop"]) for s in sig)
        lines += ["", f"<b>{len(sig)} pick{'s' if len(sig) > 1 else ''}</b> · money {_p(money, 0)}"
                      + (f" of {_p(cap, 0)}" if cap else "") + f" EGP · max loss {_p(loss, 0)} EGP",
                  "",
                  "How: buy only if the price reaches the buy level (cancel after 2 sessions). "
                  "Place the stop right after buying. No target - raise the stop after each close, never lower it.",
                  "At 11:00: below the buy level = wait · up to 2% above = OK · more than 2% above = skip."]
    over = report.get("over_budget") or []
    if over:
        lines += ["", "Over budget (not sent): " + ", ".join(e(o["symbol"]) for o in over)]
    return "\n".join(lines)


def pick(s, i):
    e = html.escape
    d = s.get("decimals", 2)
    lines = [f"<b>{i}. {e(s['symbol'])}</b> · {e(s.get('name') or '')}",
             f"Buy <b>{s['shares']:,}</b> shares at <b>{s['entry']:.{d}f}</b> (≈ {_p(s['shares'] * s['entry'], 0)} EGP)",
             f"Stop <b>{s['stop']:.{d}f}</b> · risk {_p(s['shares'] * (s['entry'] - s['stop']), 0)} EGP"]
    if s.get("t1") is not None:
        lines.append(f"Sell half at {s['t1']:.{d}f}, rest at {s['t2']:.{d}f}")
    elif s.get("trail_atr"):
        lines.append(f"Then trail the stop {_p(s['trail_atr'] * s['atr_now'], d)} under the highest price")
    if s.get("reasons"):
        lines.append("Why: " + e(s["reasons"][0]))
    for w in s.get("warnings", []):
        lines.append("⚠️ " + e(w))
    return "\n".join(lines)


def buttons(s, session):
    key = f"{s['symbol']}:{session}"
    return {"inline_keyboard": [[{"text": "✅ Bought", "callback_data": f"bought:{key}"},
                                 {"text": "👀 Watch", "callback_data": f"watch:{key}"},
                                 {"text": "❌ Skip", "callback_data": f"skip:{key}"}]]}


def messages(report, sample_note=None):
    """[(text, reply_markup or None), ...] for one morning run."""
    session = report.get("as_of") or report.get("date", "")
    out = [(header(report, sample_note), None)]
    for i, s in enumerate(report.get("signals") or [], 1):
        out.append((pick(s, i), buttons(s, session)))
    return out


def send(token, chat_id, text, markup=None, timeout=20):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": "true"}
    if markup:
        data["reply_markup"] = json.dumps(markup)
    req = urllib.request.Request(API.format(token=token, method="sendMessage"),
                                 data=urllib.parse.urlencode(data).encode())
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Send the morning picks to Telegram")
    ap.add_argument("report", help="report JSON, e.g. reports/latest.json")
    ap.add_argument("--sample-note", help="label shown on top, for test sends")
    a = ap.parse_args(argv)
    token, chat = credentials()
    if not (token and chat):
        print("telegram: skipped (TELEGRAM_TOKEN / TELEGRAM_CHAT_ID not set)")
        return 0
    report = json.load(open(a.report))
    msgs = messages(report, a.sample_note)
    ok = 0
    for text, markup in msgs:
        try:
            ok += bool(send(token, chat, text, markup).get("ok"))
        except Exception as ex:      # a failed send never fails the run
            print(f"telegram: send failed: {type(ex).__name__}")
    print(f"telegram: sent {ok}/{len(msgs)} messages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
