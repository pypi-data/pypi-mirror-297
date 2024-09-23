from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from .core import VoidWebFrame

class RequestHandler(BaseHTTPRequestHandler):
    framework = None

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        response = self.framework.handle_request(path)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode())

class Server:
    def __init__(self, framework):
        self.framework = framework

    def run(self, host='127.0.0.1', port=8080):
        RequestHandler.framework = self.framework
        server_address = (host, port)
        httpd = HTTPServer(server_address, RequestHandler)
        print(f'Starting server on {host}:{port}')
        httpd.serve_forever()