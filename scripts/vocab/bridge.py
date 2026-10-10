#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bridge: mount vocab service under /api/vocab/* on the main platform server."""
from __future__ import annotations

from urllib.parse import urlparse

from . import service


class _HostShim(service.Handler):
    """Reuse vocab Handler routes while writing responses via the host handler."""

    def __init__(self, host, path: str):
        self._host = host
        self.path = path
        self.headers = host.headers
        self.rfile = host.rfile
        self.command = getattr(host, "command", "GET")
        self.client_address = getattr(host, "client_address", ("127.0.0.1", 0))
        self.request_version = getattr(host, "request_version", "HTTP/1.1")

    def send_response(self, code, message=None):
        return self._host.send_response(code, message)

    def send_header(self, keyword, value):
        return self._host.send_header(keyword, value)

    def end_headers(self):
        return self._host.end_headers()

    @property
    def wfile(self):
        return self._host.wfile

    def log_message(self, fmt, *args):
        return


def handle_vocab_api(host_handler, method: str, student_id: str) -> None:
    """Dispatch /api/vocab/* to vocab service with a per-student DB."""
    parsed = urlparse(host_handler.path)
    rest = parsed.path[len("/api/vocab") :] or "/"
    if not rest.startswith("/"):
        rest = "/" + rest
    rewritten = "/api" + rest
    if parsed.query:
        rewritten += "?" + parsed.query

    conn = service.get_student_conn(student_id)
    shim = _HostShim(host_handler, rewritten)
    with service._LOCK:
        service.set_active_conn(conn)
        try:
            if method.upper() == "GET":
                shim.do_GET()
            else:
                shim.do_POST()
        finally:
            service.set_active_conn(None)
