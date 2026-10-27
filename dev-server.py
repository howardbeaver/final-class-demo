#!/usr/bin/env python3
"""Local dev server for MyVideoPlayer, with HTTP Range support.

`python3 -m http.server` ignores Range requests, and Safari won't play a
<video> without them. Dev only: Vercel serves the live site.

    python3 dev-server.py [port]     # default 8000 -> http://localhost:8000
"""

import os
import re
import sys
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)$")
CHUNK = 64 * 1024


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        # Revalidate every time, so edits show up on a plain reload.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def send_head(self):
        """Answer a single-range request with 206; anything else as usual."""
        self.range_length = None
        path = self.translate_path(self.path)
        match = RANGE_RE.match(self.headers.get("Range", "").strip())
        if not match or match.groups() == ("", "") or not os.path.isfile(path):
            return super().send_head()

        size = os.path.getsize(path)
        first, last = match.groups()
        if first:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        else:
            # "bytes=-N" means the last N bytes.
            start = max(size - int(last), 0)
            end = size - 1

        if start >= size or start > end:
            self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None

        f = open(path, "rb")
        f.seek(start)
        self.range_length = end - start + 1
        self.send_response(HTTPStatus.PARTIAL_CONTENT)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(self.range_length))
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        # Browsers drop video connections mid-transfer all the time (seeking,
        # switching videos). That's normal, so don't print a traceback for it.
        try:
            if self.range_length is None:
                super().copyfile(source, outputfile)
                return
            remaining = self.range_length
            while remaining:
                chunk = source.read(min(CHUNK, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    root = os.path.dirname(os.path.abspath(__file__))
    handler = partial(Handler, directory=root)
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"Serving {root} at http://localhost:{port}  (Ctrl-C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
