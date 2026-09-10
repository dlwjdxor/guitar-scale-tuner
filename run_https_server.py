import os
import sys
import socket
from functools import partial
from http.server import SimpleHTTPRequestHandler, HTTPServer

if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean_path = super().translate_path(path)
        base_dir = getattr(self, 'directory', None) or os.getcwd()
        try:
            rel_path = os.path.relpath(clean_path, base_dir)
        except Exception:
            return ""
        parts = rel_path.split(os.sep)
        for p in parts:
            # Skip current and parent path indicators
            if p in ('.', '..', ''):
                continue
            # Block hidden directories/files (.git, .env) and sensitive credentials (.pem, .key)
            if p.startswith('.') or p.endswith('.pem') or p.endswith('.key'):
                return ""  # Invalid path to block access
        return clean_path

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def find_available_port(start_port=8000, max_attempts=20):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return start_port

def run_server(port=8000, directory=None):
    if directory:
        os.chdir(directory)
    base_dir = directory or os.getcwd()
    active_port = find_available_port(port)
    server_address = ('127.0.0.1', active_port)
    handler = partial(CustomHTTPRequestHandler, directory=base_dir)
    httpd = HTTPServer(server_address, handler)
    print(f"\n===================================================")
    print(f"  Guitar Scale Tuner Server: http://localhost:{active_port}")
    print(f"===================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping Web Server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
