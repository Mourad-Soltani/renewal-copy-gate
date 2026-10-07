# Mourad.Soltani
"""Tiny stdlib HTTP service for renewal-copy-gate."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from renewal_copy_gate import __version__
from renewal_copy_gate.audit import audit_copy


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        return

    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] == "/health":
            self._send(
                200,
                {
                    "status": "ok",
                    "service": "renewal-copy-gate",
                    "version": __version__,
                    "author": "Mourad.Soltani",
                },
            )
            return
        self._send(404, {"status": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] != "/audit":
            self._send(404, {"status": "not_found"})
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send(400, {"status": "bad_request", "message": "JSON body required."})
            return
        text = data.get("text", "")
        if not isinstance(text, str):
            self._send(400, {"status": "bad_request", "message": "text must be a string."})
            return
        self._send(200, audit_copy(text))


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    serve()
