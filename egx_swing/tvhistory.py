"""Daily candle history from TradingView's chart websocket (standard library only).

Used by the scanner as the fallback when the screener's values are missing or stale,
and by the backtest to download history. Bars are split-adjusted and dated by session.
"""

import json
import random
import string
import time
from datetime import datetime, timezone

WS_URL = "wss://data.tradingview.com/socket.io/websocket?from=chart"
HEADERS = ["Origin: https://www.tradingview.com", "User-Agent: Mozilla/5.0"]


def _frame(obj):
    s = json.dumps(obj, separators=(",", ":"))
    return f"~m~{len(s)}~m~{s}"


def _split(raw):
    out, i = [], 0
    while raw.startswith("~m~", i):
        j = raw.index("~m~", i + 3)
        n = int(raw[i + 3:j])
        out.append(raw[j + 3:j + 3 + n])
        i = j + 3 + n
    return out


class _MiniWS:
    """Tiny standard-library websocket client (text frames only), so no install is needed."""

    def __init__(self, url, headers, timeout):
        import base64, os, socket, ssl
        from urllib.parse import urlparse
        u = urlparse(url)
        raw = socket.create_connection((u.hostname, 443), timeout=timeout)
        self.s = ssl.create_default_context().wrap_socket(raw, server_hostname=u.hostname)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f"GET {u.path}?{u.query} HTTP/1.1\r\nHost: {u.hostname}\r\nUpgrade: websocket\r\n"
               f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
               + "".join(h + "\r\n" for h in headers) + "\r\n")
        self.s.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = self.s.recv(4096)
            if not chunk:
                raise ConnectionError("handshake failed")
            resp += chunk
        head, self.buf = resp.split(b"\r\n\r\n", 1)
        if b" 101 " not in head.split(b"\r\n")[0]:
            raise ConnectionError(head.split(b"\r\n")[0].decode())

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.s.recv(65536)
            if not chunk:
                raise ConnectionError("closed")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _send_frame(self, opcode, payload):
        import os, struct
        hdr = bytes([0x80 | opcode])
        n = len(payload)
        if n < 126:
            hdr += bytes([0x80 | n])
        elif n < 65536:
            hdr += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            hdr += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        self.s.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))

    def send(self, text):
        self._send_frame(0x1, text.encode())

    def recv(self):
        import struct
        data = b""
        while True:
            b1, b2 = self._read(2)
            op, n = b1 & 0x0F, b2 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._read(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._read(8))[0]
            payload = self._read(n)
            if op == 0x9:
                self._send_frame(0xA, payload)
                continue
            if op == 0x8:
                raise ConnectionError("server closed")
            data += payload
            if b1 & 0x80:
                return data.decode("utf-8", "replace")

    def close(self):
        try:
            self._send_frame(0x8, b"")
            self.s.close()
        except OSError:
            pass


def _connect(timeout):
    try:
        import websocket  # websocket-client, if installed
        return websocket.create_connection(WS_URL, header=HEADERS, timeout=timeout)
    except ImportError:
        return _MiniWS(WS_URL, HEADERS, timeout)


def fetch_one(symbol, bars=800, timeout=20):
    """Return a list of dicts {date, open, high, low, close, volume}, oldest first."""
    ws = _connect(timeout)
    cs = "cs_" + "".join(random.choices(string.ascii_lowercase, k=12))
    ws.send(_frame({"m": "set_auth_token", "p": ["unauthorized_user_token"]}))
    ws.send(_frame({"m": "chart_create_session", "p": [cs, ""]}))
    ws.send(_frame({"m": "resolve_symbol", "p": [cs, "sym1", '={"symbol":"EGX:%s","adjustment":"splits"}' % symbol]}))
    ws.send(_frame({"m": "create_series", "p": [cs, "s1", "s1", "sym1", "D", bars, ""]}))
    rows, deadline = None, time.time() + timeout
    try:
        while time.time() < deadline:
            raw = ws.recv()
            for msg in _split(raw):
                if msg.startswith("~h~"):
                    ws.send(f"~m~{len(msg)}~m~{msg}")
                    continue
                try:
                    j = json.loads(msg)
                except ValueError:
                    continue
                m = j.get("m")
                if m == "timescale_update":
                    s = j["p"][1].get("s1", {}).get("s")
                    if s:
                        rows = s
                elif m in ("symbol_error", "series_error"):
                    raise RuntimeError(f"{symbol}: {m}")
                elif m == "series_completed":
                    return _to_candles(rows or [])
    finally:
        ws.close()
    raise TimeoutError(f"{symbol}: no data within {timeout}s")


def _to_candles(rows):
    out = []
    for r in rows:
        t, o, h, l, c = r["v"][:5]
        v = r["v"][5] if len(r["v"]) > 5 else 0
        d = datetime.fromtimestamp(t, tz=timezone.utc).date()
        out.append({"date": d, "open": o, "high": h, "low": l, "close": c, "volume": v})
    return out


