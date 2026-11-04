import unittest
from unittest import mock

from egx_swing import telegram
from tests.test_trend import IDX, _stock
from egx_swing import setups


class Messages(unittest.TestCase):
    def _report(self, **over):
        r = setups.scan([_stock()], IDX)
        r.update({"as_of": "2026-11-04", "run_status": "OK"}, **over)
        return r

    def test_header_plus_one_card_per_pick_with_buttons(self):
        msgs = telegram.messages(self._report())
        self.assertEqual(len(msgs), 2)
        self.assertIsNone(msgs[0][1])
        keys = [b["callback_data"] for b in msgs[1][1]["inline_keyboard"][0]]
        self.assertEqual(keys, ["bought:TRND:2026-11-04", "watch:TRND:2026-11-04", "skip:TRND:2026-11-04"])
        self.assertIn("trail the stop", msgs[1][0])

    def test_no_picks_says_no_buys(self):
        r = self._report(); r["signals"] = []
        self.assertIn("No new buys today", telegram.messages(r)[0][0])

    def test_html_is_escaped(self):
        r = self._report(); r["signals"][0]["name"] = "A & B <x>"
        self.assertIn("A &amp; B &lt;x&gt;", telegram.messages(r)[1][0])

    def test_skips_quietly_without_credentials(self):
        with mock.patch.object(telegram, "credentials", return_value=(None, None)), \
             mock.patch.object(telegram, "send") as s:
            self.assertEqual(telegram.main(["x.json"]), 0)
            s.assert_not_called()


if __name__ == "__main__":
    unittest.main()
