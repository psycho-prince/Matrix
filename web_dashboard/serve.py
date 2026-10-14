#!/usr/bin/env python3
"""
Simple HTTP server to serve the Memory Economics Interactive Web Dashboard.
"""
import http.server
import socketserver
import os
import webbrowser

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"===========================================================")
        print(f"  Matrix: Generational Artificial Life - Web Dashboard")
        print(f"  Local URL: http://localhost:{PORT}")
        print(f"===========================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
