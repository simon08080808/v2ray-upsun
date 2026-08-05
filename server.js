import os
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

TARGET_HOST = "simon.benbilal237free.xyz"
TARGET_PORT = 80

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class RelayHandler(BaseHTTPRequestHandler):
    def do_relay(self):
        url = f"http://{TARGET_HOST}:{TARGET_PORT}{self.path}"
        headers = {k: v for k, v in self.headers.items() if k.lower() != 'host'}
        headers['Host'] = TARGET_HOST

        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len) if content_len > 0 else None

        req = urllib.request.Request(url, data=body, headers=headers, method=self.command)

        try:
            with urllib.request.urlopen(req) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for k, v in e.headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception:
            self.send_error(502, "Bad Gateway")

    def do_GET(self): self.do_relay()
    def do_POST(self): self.do_relay()
    def do_PUT(self): self.do_relay()
    def do_OPTIONS(self): self.do_relay()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = ThreadedHTTPServer(("0.0.0.0", port), RelayHandler)
    server.serve_forever()
