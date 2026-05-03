from __future__ import annotations

import argparse
import functools
import http.server
import os
import posixpath
import socketserver
import threading
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .build import OUT_DIR, ROOT_DIR, build


WATCH_PATHS = [
    ROOT_DIR / "README.md",
    ROOT_DIR / "content",
    ROOT_DIR / "public",
    ROOT_DIR / "src" / "builder",
]

RELOAD_SCRIPT = """
<script>
(() => {
  let version = null;
  async function check() {
    try {
      const response = await fetch('/__reload-version', { cache: 'no-store' });
      const nextVersion = await response.text();
      if (version === null) {
        version = nextVersion;
      } else if (version !== nextVersion) {
        window.location.reload();
      }
    } catch (error) {
      // The dev server may be rebuilding; try again on the next tick.
    }
  }
  setInterval(check, 500);
  check();
})();
</script>
"""


class ReloadState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._version = 0

    @property
    def version(self) -> int:
        with self._lock:
            return self._version

    def bump(self) -> None:
        with self._lock:
            self._version += 1


class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, reload_state: ReloadState, **kwargs):
        self.reload_state = reload_state
        super().__init__(*args, **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:
        if self.path == "/__reload-version":
            body = str(self.reload_state.version).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            for index in ("index.html", "index.htm"):
                index_path = os.path.join(path, index)
                if os.path.exists(index_path):
                    path = index_path
                    break
            else:
                return self.list_directory(path)

        if not path.endswith(".html"):
            return super().send_head()

        try:
            content = Path(path).read_text(encoding="utf-8")
        except OSError:
            self.send_error(404, "File not found")
            return None

        content = inject_reload_script(content).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        return BytesReader(content)

    def translate_path(self, path):
        # Keep the stdlib path normalization, but serve from OUT_DIR explicitly.
        path = urlsplit(path).path
        path = posixpath.normpath(unquote(path))
        words = [word for word in path.split("/") if word]
        resolved = OUT_DIR
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue
            resolved = resolved / word
        return str(resolved)


class BytesReader:
    def __init__(self, body: bytes) -> None:
        self.body = body
        self.offset = 0

    def read(self, size: int = -1) -> bytes:
        if size == -1:
            size = len(self.body) - self.offset
        chunk = self.body[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk

    def close(self) -> None:
        pass


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def inject_reload_script(content: str) -> str:
    if "</body>" in content:
        return content.replace("</body>", f"{RELOAD_SCRIPT}</body>")
    return f"{content}{RELOAD_SCRIPT}"


def watch(reload_state: ReloadState, interval: float) -> None:
    snapshot = file_snapshot()
    while True:
        time.sleep(interval)
        next_snapshot = file_snapshot()
        if next_snapshot == snapshot:
            continue

        print("Change detected. Rebuilding...")
        try:
            build()
        except Exception as error:
            print(f"Build failed: {error}")
        else:
            snapshot = file_snapshot()
            reload_state.bump()
            print("Build complete.")


def file_snapshot() -> dict[Path, int]:
    return {
        path: path.stat().st_mtime_ns
        for root in WATCH_PATHS
        for path in iter_files(root)
    }


def iter_files(path: Path):
    if path.is_file():
        yield path
        return
    if not path.exists():
        return
    for child in path.rglob("*"):
        if should_watch(child):
            yield child


def should_watch(path: Path) -> bool:
    return (
        path.is_file()
        and not path.name.startswith(".")
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument("--interval", default=0.5, type=float)
    args = parser.parse_args()

    build()
    reload_state = ReloadState()
    watcher = threading.Thread(
        target=watch,
        args=(reload_state, args.interval),
        daemon=True,
    )
    watcher.start()

    handler = functools.partial(StaticHandler, reload_state=reload_state)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving http://{args.host}:{args.port}")
    print("Watching README.md, content/, public/, and src/builder/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
