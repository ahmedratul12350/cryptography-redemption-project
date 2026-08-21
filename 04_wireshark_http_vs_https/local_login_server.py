"""
LOCAL LAB ONLY.
Runs a tiny login-form server for comparing HTTP and HTTPS packet visibility.
Use only dummy credentials on your own machine.
"""

import argparse
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

FORM = b"""<!doctype html>
<html>
<head><meta charset='utf-8'><title>Local Crypto Lab Login</title></head>
<body>
<h2>Local HTTP vs HTTPS Lab</h2>
<p>Use dummy credentials only.</p>
<form method='POST' action='/login'>
  <label>Username: <input name='username'></label><br><br>
  <label>Password: <input type='password' name='password'></label><br><br>
  <button type='submit'>Submit</button>
</form>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(FORM)))
        self.end_headers()
        self.wfile.write(FORM)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        fields = parse_qs(raw.decode("utf-8", errors="replace"))
        username = fields.get("username", ["(missing)"])[0]

        # Intentionally do not print the password to the terminal.
        body = (
            "Lab form received. Use Wireshark to compare how the same POST "
            "looks over HTTP and HTTPS.\n"
            f"Dummy username received: {username}\n"
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--https", action="store_true", help="Serve using TLS")
    parser.add_argument("--cert", default="cert.pem")
    parser.add_argument("--key", default="key.pem")
    args = parser.parse_args()

    port = 18443 if args.https else 18080
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)

    scheme = "http"
    if args.https:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=args.cert, keyfile=args.key)
        server.socket = context.wrap_socket(server.socket, server_side=True)
        scheme = "https"

    print(f"Local lab server: {scheme}://127.0.0.1:{port}")
    print("Use DUMMY credentials only. Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
