#!/usr/bin/env python3
"""Mini-Server: nimmt POST /save?name=x.jpg entgegen und speichert nach assets/personal/."""
import pathlib
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/personal"
OUT.mkdir(parents=True, exist_ok=True)
SAFE = re.compile(r"^[a-z0-9_-]{1,40}\.(jpg|png|webp)$")


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        name = (self.path.split("name=", 1) + [""])[1]
        if not SAFE.match(name):
            self.send_response(400)
            self._cors()
            self.end_headers()
            return
        n = int(self.headers.get("Content-Length", 0))
        if 0 < n < 30_000_000:
            (OUT / name).write_bytes(self.rfile.read(n))
            self.send_response(200)
        else:
            self.send_response(400)
        self._cors()
        self.end_headers()

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("127.0.0.1", 4174), H).serve_forever()
