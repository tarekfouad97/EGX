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


# ───────────────────────────── HTML email ─────────────────────────────
# Table-based layout with inline styles (what Gmail/Outlook render reliably) plus a
# small <style> block whose media query stacks columns on phones.

C = {"bg": "#f1f5f9", "card": "#ffffff", "ink": "#0f172a", "muted": "#64748b", "line": "#e2e8f0",
     "navy": "#0f172a", "green": "#047857", "green_bg": "#ecfdf5", "red": "#b91c1c", "red_bg": "#fef2f2",
     "amber": "#92400e", "amber_bg": "#fffbeb", "blue": "#1d4ed8", "blue_bg": "#eff6ff"}
STATUS = {"OK": ("#047857", "#d1fae5"), "DEGRADED": ("#92400e", "#fef3c7"),
          "FAILED": ("#b91c1c", "#fee2e2"), "OFFLINE": ("#334155", "#e2e8f0")}
REGIME = {"RISK-ON": ("#047857", "#d1fae5"), "NEUTRAL": ("#92400e", "#fef3c7"),
          "RISK-OFF": ("#b91c1c", "#fee2e2"), "UNKNOWN": ("#334155", "#e2e8f0")}
FONT = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif'  # used inside '...' attrs

CSS = """
body{margin:0;padding:0;background:#f1f5f9}
table{border-collapse:collapse}
a{color:#1d4ed8}
@media only screen and (max-width:620px){
  .wrap{width:100%!important}
  .pad{padding-left:16px!important;padding-right:16px!important}
  .stack{display:block!important;width:100%!important;box-sizing:border-box}
  .half{display:inline-block!important;width:50%!important;box-sizing:border-box}
  .h1{font-size:22px!important}
  .big{font-size:20px!important}
}
"""


def _pill(text, fg, bg):
    return (f"<span style='display:inline-block;padding:3px 10px;border-radius:999px;background:{bg};"
            f"color:{fg};font-size:12px;font-weight:700;letter-spacing:.3px'>{html.escape(text)}</span>")


def _tile(label, value, fg, bg):
    return (f"<td class='stack' width='33%' style='padding:6px'>"
            f"<div style='background:{bg};border-radius:12px;padding:14px 16px'>"
            f"<div style='font-size:12px;color:{C['muted']};text-transform:uppercase;letter-spacing:.5px'>{label}</div>"
            f"<div class='big' style='font-size:22px;font-weight:800;color:{fg};margin-top:4px'>{value}</div>"
            f"</div></td>")


def _level(label, value, fg, bg):
    return (f"<td class='half' width='25%' style='padding:4px'>"
            f"<div style='background:{bg};border-radius:10px;padding:10px 12px;text-align:center'>"
            f"<div style='font-size:11px;color:{C['muted']}'>{label}</div>"
            f"<div style='font-size:17px;font-weight:800;color:{fg};margin-top:2px'>{value}</div>"
            f"</div></td>")


def _card(r):
    e = html.escape
    s = r["s"]
    warn = "".join(
        f"<div style='background:{C['amber_bg']};color:{C['amber']};border-radius:8px;padding:8px 12px;"
        f"font-size:13px;margin-top:8px'>&#9888; {e(w)}</div>" for w in s.get("warnings", []))
    return (
        f"<tr><td class='pad' style='padding:8px 24px'>"
        f"<table width='100%' style='background:{C['card']};border:1px solid {C['line']};border-radius:14px'>"
        f"<tr><td style='padding:18px 18px 6px'>"
        f"<table width='100%'><tr>"
        f"<td style='vertical-align:top'><div style='font-size:22px;font-weight:800;color:{C['ink']}'>{e(s['symbol'])}</div>"
        f"<div style='font-size:13px;color:{C['muted']}'>{e(s.get('name', ''))}</div></td>"
        f"<td style='text-align:right;vertical-align:top'>"
        f"{_pill(s['setup'], C['blue'], C['blue_bg']) if s.get('setup') else ''}</td>"
        f"</tr></table>"
        f"<div style='font-size:15px;color:{C['ink']};margin:12px 0 4px;line-height:1.5'>"
        f"Buy <b>{s['shares']:,} shares</b> only once the price reaches <b>{_p(s['entry'])} EGP</b> "
        f"&middot; about <b>{_p(r['money'], 0)} EGP</b></div>"
        f"</td></tr>"
        f"<tr><td style='padding:6px 14px 4px'><table width='100%'><tr>"
        + _level("Buy at", _p(s["entry"]), C["blue"], C["blue_bg"])
        + _level("Stop-loss", _p(s["stop"]), C["red"], C["red_bg"])
        + _level("Sell half at", _p(s["t1"]), C["green"], C["green_bg"])
        + _level("Sell rest at", _p(s["t2"]), C["green"], C["green_bg"])
        + f"</tr></table></td></tr>"
        f"<tr><td style='padding:4px 18px 16px;font-size:13px;color:{C['muted']}'>"
        f"Risk if stopped: <b style='color:{C['red']}'>-{_p(r['loss'], 0)} EGP</b> &nbsp;&middot;&nbsp; "
        f"Best case: <b style='color:{C['green']}'>+{_p(r['best'], 0)} EGP</b>{warn}</td></tr>"
        f"</table></td></tr>")


def html_body(report, run_url=None):
    e = html.escape
    rows = plan_rows(report)
    reg = report.get("regime") or {}
    idx = report.get("index") or {}
    status = report.get("run_status", "?")
    cap = (report.get("config") or {}).get("capital")
    sfg, sbg = STATUS.get(status, STATUS["OFFLINE"])
    rfg, rbg = REGIME.get(reg.get("regime"), REGIME["UNKNOWN"])

    market = _pill(reg.get("regime", "?"), rfg, rbg)
    if _num(idx.get("close")):
        chg = idx.get("perf_1m")
        col = C["green"] if _num(chg) and chg >= 0 else C["red"]
        market += (f" &nbsp;<span style='color:{C['ink']};font-weight:700'>EGX30 {idx['close']:,.0f}</span>"
                   + (f" <span style='color:{col};font-weight:700'>{chg:+.1f}% 1M</span>" if _num(chg) else ""))

    body = [
        # header
        f"<tr><td class='pad' style='background:{C['navy']};padding:26px 24px;border-radius:16px 16px 0 0'>"
        f"<div style='font-size:12px;color:#94a3b8;letter-spacing:1px;text-transform:uppercase'>EGX swing trader</div>"
        f"<div class='h1' style='font-size:26px;font-weight:800;color:#ffffff;margin:4px 0 10px'>"
        f"Picks for the next session</div>"
        f"<span style='color:#cbd5e1;font-size:14px'>Data: session {e(str(report.get('as_of') or '?'))}</span>"
        f" &nbsp;{_pill(status, sfg, sbg)}</td></tr>",
        # market strip
        f"<tr><td class='pad' style='background:{C['card']};padding:14px 24px;border-bottom:1px solid {C['line']}'>"
        f"{market}<div style='font-size:13px;color:{C['muted']};margin-top:6px'>{e(reg.get('note', ''))}</div>"
        f"</td></tr>",
    ]
    if status == "FAILED":
        body.append(f"<tr><td class='pad' style='padding:16px 24px'><div style='background:{C['red_bg']};"
                    f"color:{C['red']};border-radius:12px;padding:14px 16px;font-weight:700'>"
                    f"No usable market data this run - no trades.</div></td></tr>")
    if not rows:
        body.append(f"<tr><td class='pad' style='padding:24px;text-align:center'>"
                    f"<div style='font-size:18px;font-weight:800;color:{C['ink']}'>No setups today</div>"
                    f"<div style='color:{C['muted']};margin-top:4px'>Cash is a position.</div></td></tr>")
    else:
        money, loss, best = (sum(r[k] for r in rows) for k in ("money", "loss", "best"))
        of = f"<div style='font-size:12px;color:{C['muted']}'>of {_p(cap, 0)} EGP</div>" if _num(cap) else ""
        body.append(
            f"<tr><td class='pad' style='padding:16px 18px 4px'><table width='100%'><tr>"
            + _tile("Money used", f"{_p(money, 0)}{of}", C["ink"], "#f1f5f9")
            + _tile("Most you can lose", f"-{_p(loss, 0)}", C["red"], C["red_bg"])
            + _tile("Best case", f"+{_p(best, 0)}", C["green"], C["green_bg"])
            + "</tr></table></td></tr>")
        body += [_card(r) for r in rows]
    if report.get("vetoed"):
        names = ", ".join(e(s["symbol"]) for s in report["vetoed"])
        body.append(f"<tr><td class='pad' style='padding:8px 24px'><div style='background:{C['red_bg']};"
                    f"color:{C['red']};border-radius:12px;padding:12px 16px'><b>Don't buy:</b> {names}"
                    f" (vetoed by AI review)</div></td></tr>")
    steps = ["<b>Don't buy at the open.</b> Wait for the price to <i>rise to</i> the buy price - use a "
             "stop-buy order, or a price alert.",
             "<b>Not reached within 2 trading days?</b> Don't buy; cancel the order.",
             "<b>Right after buying,</b> place a stop-loss sell order at the stop-loss price.",
             "<b>At \"sell half at\",</b> sell half and move the stop on the rest up to your buy price.",
             "<b>Sell the rest</b> at the final price, or after about 10 trading days."]
    body.append(
        f"<tr><td class='pad' style='padding:16px 24px 8px'>"
        f"<div style='font-size:16px;font-weight:800;color:{C['ink']};margin-bottom:8px'>How to do it</div>"
        + "".join(f"<table width='100%' style='margin-bottom:6px'><tr>"
                  f"<td width='28' style='vertical-align:top'><div style='width:22px;height:22px;border-radius:11px;"
                  f"background:{C['navy']};color:#fff;font-size:12px;font-weight:700;text-align:center;"
                  f"line-height:22px'>{i}</div></td>"
                  f"<td style='font-size:14px;color:{C['ink']};line-height:1.5'>{t}</td></tr></table>"
                  for i, t in enumerate(steps, 1))
        + "</td></tr>")
    body.append(
        f"<tr><td class='pad' style='padding:8px 24px 20px'>"
        f"<div style='background:{C['blue_bg']};border-radius:12px;padding:12px 16px;font-size:14px;color:{C['ink']}'>"
        f"These are the scanner's chart picks at full size. For the news-checked answer "
        f"(TAKE / TAKE SMALLER / SKIP), run <b>/egx-swing-review</b> in Claude Code before buying.</div>"
        + (f"<div style='text-align:center;margin-top:18px'><a href='{e(run_url)}' style='display:inline-block;"
           f"background:{C['navy']};color:#ffffff;text-decoration:none;font-weight:700;padding:12px 22px;"
           f"border-radius:10px'>Open the full report on GitHub</a></div>" if run_url else "")
        + "</td></tr>")
    body.append(
        f"<tr><td class='pad' style='padding:16px 24px;border-top:1px solid {C['line']};font-size:12px;"
        f"color:{C['muted']};text-align:center'>Full report attached &middot; Analytical output only - "
        f"not licensed financial advice.</td></tr>")

    preheader = e(text_body(report).splitlines()[0])
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<meta name='color-scheme' content='light'><meta name='supported-color-schemes' content='light'>"
            f"<style>{CSS}</style></head>"
            f"<body style='margin:0;padding:0;background:{C['bg']};font-family:{FONT}'>"
            f"<div style='display:none;max-height:0;overflow:hidden;opacity:0'>{preheader}</div>"
            f"<table width='100%' style='background:{C['bg']}'><tr><td align='center' style='padding:20px 8px'>"
            f"<table class='wrap' width='640' style='width:640px;max-width:640px;background:{C['card']};"
            f"border-radius:16px;font-family:{FONT}'>"
            + "".join(body) +
            "</table></td></tr></table></body></html>")


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
