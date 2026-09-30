from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from cortex_session import CortexSession


session = CortexSession()


class ApiHandler(BaseHTTPRequestHandler):
    def _respond(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5174"))
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._respond(HTTPStatus.NO_CONTENT, {})

    def do_GET(self) -> None:
        if self.path == "/api/health":
            self._respond(HTTPStatus.OK, {"ok": True})
        elif self.path == "/api/session":
            self._respond(HTTPStatus.OK, session.snapshot())
        else:
            self._respond(HTTPStatus.NOT_FOUND, {"error": "Route not found"})

    def do_POST(self) -> None:
        if self.path == "/api/session/start":
            self._start_session()
        elif self.path == "/api/session/stop":
            self._respond(HTTPStatus.OK, session.stop())
        else:
            self._respond(HTTPStatus.NOT_FOUND, {"error": "Route not found"})

    def _start_session(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length) or b"{}")
            payload = session.start(body.get("headsetId"), body.get("streams"))
            self._respond(HTTPStatus.ACCEPTED, payload)
        except (ValueError, RuntimeError) as error:
            self._respond(HTTPStatus.BAD_REQUEST, {"error": str(error)})

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    host = os.getenv("CORTEX_API_HOST", "127.0.0.1")
    port = int(os.getenv("CORTEX_API_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), ApiHandler)
    print(f"Cortex API bridge listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()