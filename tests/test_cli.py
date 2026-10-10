import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

import egx_swing.cli as cli


class Emergency(unittest.TestCase):
    def test_unexpected_error_still_writes_report(self):
        class Boom:
            def __init__(self, **kw):
                pass

            def run(self, *a):
                raise RuntimeError("unexpected bug")

        orig, cli.Run = cli.Run, Boom
        try:
            with tempfile.TemporaryDirectory() as d, redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                rc = cli.main(["--out-dir", d, "--cache", os.path.join(d, "u.json")])
                files = sorted(os.listdir(d))
                with open(os.path.join(d, "latest.md"), encoding="utf-8") as f:
                    md = f.read()
                dated = [x for x in files if x.endswith("-FAILED.json")]
                with open(os.path.join(d, dated[0]), encoding="utf-8") as f:
                    data = json.load(f)
        finally:
            cli.Run = orig
        self.assertEqual(rc, 0)
        self.assertIn("Run status: **FAILED**", md)
        self.assertIn("RuntimeError: unexpected bug", md)
        self.assertEqual(data["run_status"], "FAILED")
        self.assertIn("latest.json", files)


if __name__ == "__main__":
    unittest.main()
