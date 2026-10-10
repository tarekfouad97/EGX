"""Email the scan report: python -m egx_swing.notify reports/latest.json [--run-url URL]

Settings come from environment variables (GitHub repository secrets in the workflow):
    SMTP_USERNAME   sender login, e.g. you@gmail.com            (required)
    SMTP_PASSWORD   for Gmail, an App Password - not your login (required)
    MAIL_TO         recipient(s), comma-separated; default = SMTP_USERNAME
    SMTP_HOST       default smtp.gmail.com
    SMTP_PORT       default 465 (SSL)

Without SMTP_USERNAME/SMTP_PASSWORD it prints "skipped" and exits 0: email is optional
and must never break the scan or the report commit.
"""

import argparse
import html
import json
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _p(v, d=2):
    return f"{v:,.{d}f}" if _num(v) else "n/a"


def plan_rows(report):
    rows = []
    for s in report.get("signals", []):
        n, e = s.get("shares") or 0, s.get("entry")
        if not (n and _num(e)):
            continue
        half, rest = n // 2, n - n // 2
        best = half * (s["t1"] - e) + rest * (s["t2"] - e)
        rows.append({"s": s, "money": n * e, "loss": n * (e - s["stop"]), "best": best})
    return rows


def subject(report):
    rows = plan_rows(report)
    status = report.get("run_status", "?")
    picks = ", ".join(r["s"]["symbol"] for r in rows) or "no setups"
    return f"EGX swing scan {report.get('as_of') or report.get('date', '')} - {picks} [{status}]"


def text_body(report, run_url=None):
    rows = plan_rows(report)
    reg = report.get("regime") or {}
    cap = (report.get("config") or {}).get("capital")
    out = [subject(report), "",
           f"Market: {reg.get('regime', '?')} - {reg.get('note', '')}", ""]
    if report.get("run_status") == "FAILED":
        out += ["NO USABLE DATA THIS RUN - NO TRADES.", ""]
    if not rows:
        out += ["No setups today. Cash is a position.", ""]
    for r in rows:
        s = r["s"]
        out.append(f"{s['symbol']} ({s.get('name', '')}): buy {s['shares']} shares only once price reaches "
                   f"{_p(s['entry'])} (~{_p(r['money'], 0)} EGP). Stop {_p(s['stop'])}. "
                   f"Sell half at {_p(s['t1'])}, rest at {_p(s['t2'])}.")
        out += [f"   ! {w}" for w in s.get("warnings", [])]
    if rows:
        money, loss, best = (sum(r[k] for r in rows) for k in ("money", "loss", "best"))
        out += ["", f"Total money used: ~{_p(money, 0)} EGP" + (f" of {_p(cap, 0)}" if _num(cap) else ""),
                f"Most you can lose (all stops hit): ~{_p(loss, 0)} EGP",
                f"Best case (all targets hit): +{_p(best, 0)} EGP"]
    for s in report.get("vetoed", []):
        out.append(f"DON'T BUY {s['symbol']}: vetoed by AI review.")
    out += ["", "How: wait for the price to rise to the buy price (stop-buy order or price alert); cancel after 2 "
            "trading days if not reached; place the stop-loss right after buying; sell half at the first target "
            "and move the stop to your buy price.", ""]
    if run_url:
        out.append(f"Full run: {run_url}")
    out.append("Analytical output only - not licensed financial advice.")
    return "\n".join(out)


def html_body(report, run_url=None):
    e = html.escape
    rows = plan_rows(report)
    reg = report.get("regime") or {}
    status = report.get("run_status", "?")
    cap = (report.get("config") or {}).get("capital")
    td = 'style="padding:6px 10px;border-bottom:1px solid #ddd;text-align:right"'
    th = 'style="padding:6px 10px;border-bottom:2px solid #333;text-align:right;background:#f4f4f4"'
    parts = [f"<h2 style='margin:0 0 4px'>EGX swing scan - session {e(str(report.get('as_of') or '?'))}</h2>",
             f"<p style='margin:0 0 12px;color:#555'>Run status: <b>{e(status)}</b> &middot; "
             f"Market: <b>{e(reg.get('regime', '?'))}</b> - {e(reg.get('note', ''))}</p>"]
    if status == "FAILED":
        parts.append("<p style='color:#b00020'><b>No usable market data this run - no trades.</b></p>")
    if not rows:
        parts.append("<p><b>No setups today.</b> Cash is a position.</p>")
    else:
        heads = ["Stock", "Buy shares", "Only once price reaches", "Money needed", "Sell all if it drops to",
                 "Sell half at", "Sell rest at"]
        parts.append("<table style='border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px'><tr>"
                     + "".join(f"<th {th}>{h}</th>" for h in heads) + "</tr>")
        for r in rows:
            s = r["s"]
            cells = [f"<b>{e(s['symbol'])}</b><br><span style='color:#666'>{e(s.get('name', ''))}</span>",
                     f"{s['shares']:,}", _p(s["entry"]), f"~{_p(r['money'], 0)}", _p(s["stop"]),
                     _p(s["t1"]), _p(s["t2"])]
            parts.append("<tr>" + "".join(f"<td {td}>{c}</td>" for c in cells) + "</tr>")
        parts.append("</table>")
        money, loss, best = (sum(r[k] for r in rows) for k in ("money", "loss", "best"))
        of = f" of {_p(cap, 0)}" if _num(cap) else ""
        parts.append(f"<p><b>Total money used:</b> ~{_p(money, 0)} EGP{of}<br>"
                     f"<b>Most you can lose</b> (all stops hit): ~{_p(loss, 0)} EGP<br>"
                     f"<b>Best case</b> (all targets hit): +{_p(best, 0)} EGP</p>")
        warn = [(r["s"]["symbol"], w) for r in rows for w in r["s"].get("warnings", [])]
        if warn:
            parts.append("<p><b>Warnings</b></p><ul>"
                         + "".join(f"<li>{e(sym)}: {e(w)}</li>" for sym, w in warn) + "</ul>")
    if report.get("vetoed"):
        parts.append("<p style='color:#b00020'><b>Don't buy:</b> "
                     + ", ".join(e(s["symbol"]) for s in report["vetoed"]) + " (vetoed by AI review)</p>")
    parts.append("<p><b>How to do it:</b></p><ol>"
                 "<li>Don't buy at the open - wait for the price to <i>rise to</i> the buy price "
                 "(stop-buy order, or a price alert).</li>"
                 "<li>Not reached within 2 trading days? Don't buy; cancel the order.</li>"
                 "<li>Right after buying, place a stop-loss sell order at the 'drops to' price.</li>"
                 "<li>At 'sell half at', sell half and move the stop on the rest up to your buy price.</li>"
                 "<li>Sell the rest at the final price, or after ~10 trading days.</li></ol>")
    parts.append("<p style='color:#555'>For news and fundamentals on these picks, run "
                 "<code>/egx-swing-review</code> in Claude Code. The full report is attached.</p>")
    if run_url:
        parts.append(f"<p><a href='{e(run_url)}'>Open the GitHub run</a></p>")
    parts.append("<p style='color:#888;font-size:12px'>Analytical output only - not licensed financial advice.</p>")
    return "<html><body style='font-family:Arial,sans-serif'>" + "".join(parts) + "</body></html>"


def build_message(report, sender, to, run_url=None, attachment=None):
    msg = EmailMessage()
    msg["Subject"] = subject(report)
    msg["From"] = sender
    msg["To"] = ", ".join(to)
    msg.set_content(text_body(report, run_url))
    msg.add_alternative(html_body(report, run_url), subtype="html")
    if attachment and os.path.exists(attachment):
        with open(attachment, "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="markdown",
                               filename=os.path.basename(attachment))
    return msg


def send(msg, host, port, user, password):
    with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context(), timeout=30) as s:
        s.login(user, password)
        s.send_message(msg)


def main(argv=None, env=None):
    env = os.environ if env is None else env
    ap = argparse.ArgumentParser(prog="egx_swing.notify", description="Email the swing scan report")
    ap.add_argument("report", help="path to latest.json")
    ap.add_argument("--run-url", help="link to the workflow run")
    args = ap.parse_args(argv)

    user, password = env.get("SMTP_USERNAME"), env.get("SMTP_PASSWORD")
    if not (user and password):
        print("email skipped: SMTP_USERNAME / SMTP_PASSWORD not set")
        return 0
    to = [a.strip() for a in (env.get("MAIL_TO") or user).split(",") if a.strip()]
    try:
        with open(args.report, encoding="utf-8") as f:
            report = json.load(f)
        md = os.path.join(os.path.dirname(args.report), "latest.md")
        msg = build_message(report, user, to, args.run_url, attachment=md)
        send(msg, env.get("SMTP_HOST", "smtp.gmail.com"), int(env.get("SMTP_PORT", "465")), user, password)
    except Exception as e:          # never fail the workflow over email
        print(f"email FAILED: {type(e).__name__}: {e}", file=sys.stderr)
        return 0
    print(f"email sent to {len(to)} recipient(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
