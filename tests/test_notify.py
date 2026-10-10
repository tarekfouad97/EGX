import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest import mock

from egx_swing import notify

PICK = {"symbol": "ABUK", "name": "Abou Kir <Fert>", "shares": 72, "entry": 90.32, "stop": 83.38,
        "t1": 100.73, "t2": 111.14, "warnings": ["1M high 96.29 sits below T1 - resistance"]}
REPORT = {"as_of": "2026-10-07", "run_status": "DEGRADED", "regime": {"regime": "RISK-OFF", "note": "risk halved"},
          "config": {"capital": 100000.0}, "signals": [PICK], "vetoed": [{"symbol": "XYZ"}]}


class Body(unittest.TestCase):
    def test_totals(self):
        r = notify.plan_rows(REPORT)[0]
        self.assertAlmostEqual(r["money"], 72 * 90.32)
        self.assertAlmostEqual(r["loss"], 72 * (90.32 - 83.38))
        self.assertAlmostEqual(r["best"], 36 * (100.73 - 90.32) + 36 * (111.14 - 90.32))

    def test_subject(self):
        self.assertEqual(notify.subject(REPORT), "EGX swing scan 2026-10-07 - ABUK [DEGRADED]")
        self.assertIn("no setups", notify.subject({**REPORT, "signals": []}))

    def test_html_escapes_and_contains_plan(self):
        h = notify.html_body(REPORT, "https://x/run")
        self.assertIn("Abou Kir &lt;Fert&gt;", h)
        self.assertNotIn("<Fert>", h)
        self.assertIn("@media only screen", h)            # responsive
        self.assertNotIn("'Segoe UI'", h)                  # no quote clash inside style='...' 
        for v in ("90.32", "83.38", "100.73", "111.14", "6,503", "+1,124", "XYZ", "https://x/run"):
            self.assertIn(v, h)

    def test_text_body_failed_run(self):
        t = notify.text_body({**REPORT, "run_status": "FAILED", "signals": []})
        self.assertIn("NO TRADES", t)
        self.assertIn("No setups today", t)

    def test_message_has_html_and_attachment(self):
        with tempfile.TemporaryDirectory() as d:
            md = os.path.join(d, "latest.md")
            with open(md, "w") as f:
                f.write("# report")
            msg = notify.build_message(REPORT, "a@x.com", ["b@x.com"], attachment=md)
        types = [p.get_content_type() for p in msg.walk()]
        self.assertIn("text/html", types)
        self.assertIn("text/markdown", types)
        self.assertEqual(msg["To"], "b@x.com")


class Main(unittest.TestCase):
    def _report_file(self, d):
        p = os.path.join(d, "latest.json")
        with open(p, "w") as f:
            json.dump(REPORT, f)
        return p

    def test_skipped_without_credentials(self):
        with tempfile.TemporaryDirectory() as d, redirect_stdout(StringIO()) as out:
            self.assertEqual(notify.main([self._report_file(d)], env={}), 0)
        self.assertIn("skipped", out.getvalue())

    def test_sends_to_mail_to(self):
        env = {"SMTP_USERNAME": "me@gmail.com", "SMTP_PASSWORD": "pw", "MAIL_TO": "a@x.com, b@x.com"}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(notify, "send") as send, \
                redirect_stdout(StringIO()):
            self.assertEqual(notify.main([self._report_file(d)], env=env), 0)
        msg, host, port, user, pw = send.call_args[0]
        self.assertEqual(msg["To"], "a@x.com, b@x.com")
        self.assertEqual((host, port, user), ("smtp.gmail.com", 465, "me@gmail.com"))

    def test_send_failure_never_fails_the_job(self):
        env = {"SMTP_USERNAME": "me@gmail.com", "SMTP_PASSWORD": "pw"}
        with tempfile.TemporaryDirectory() as d, \
                mock.patch.object(notify, "send", side_effect=OSError("smtp down")), \
                redirect_stderr(StringIO()) as err:
            self.assertEqual(notify.main([self._report_file(d)], env=env), 0)
        self.assertIn("email FAILED", err.getvalue())


if __name__ == "__main__":
    unittest.main()
