import http.server
import socketserver
import requests
from PyQt6.QtCore import QThread, pyqtSignal
from functools import partial

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    """
    The request handler for the proxy server. It forwards requests and uses
    a signal to log messages back to the main GUI thread.
    """
    def __init__(self, *args, log_signal=None, upstream_host=None, **kwargs):
        self.log_signal = log_signal
        self.upstream_host = upstream_host
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self._forward_request("GET")

    def do_POST(self):
        self._forward_request("POST")

    def do_PUT(self):
        self._forward_request("PUT")

    def do_DELETE(self):
        self._forward_request("DELETE")
        
    def do_HEAD(self):
        self._forward_request("HEAD")

    def _forward_request(self, method):
        """
        Forwards the incoming request and logs information using the provided signal.
        """
        if not self.upstream_host:
            self.send_error(500, "Upstream host not configured.")
            if self.log_signal:
                self.log_signal.emit("[ERROR] Proxy forwarding failed: Upstream host not configured.")
            return

        upstream_url = f"{self.upstream_host}{self.path}"
        
        if self.log_signal:
            self.log_signal.emit(f"--> {method} {self.path} to {self.upstream_host}")

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        headers = {key: value for key, value in self.headers.items() if key.lower() != 'host'}

        try:
            response = requests.request(
                method, upstream_url, headers=headers, data=body, stream=True, timeout=30
            )

            if self.log_signal:
                self.log_signal.emit(f"<-- {response.status_code} from {upstream_url}")

            self.send_response(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ('transfer-encoding', 'content-encoding', 'connection'):
                    self.send_header(key, value)
            self.end_headers()

            if response.content:
                self.wfile.write(response.content)

        except requests.exceptions.RequestException as e:
            if self.log_signal:
                self.log_signal.emit(f"[ERROR] Proxy error: {e}")
            self.send_error(502, f"Proxy error: {e}")

class ProxyThread(QThread):
    """
    Runs the proxy server in a separate thread.
    """
    log_message = pyqtSignal(str)

    def __init__(self, port, upstream_host):
        super().__init__()
        self.port = port
        self.upstream_host = upstream_host
        self.httpd = None

    def run(self):
        """The entry point for the thread."""
        try:
            # Create a handler class with our signal and upstream host partially filled in
            HandlerWithLogging = partial(
                ProxyHandler, 
                log_signal=self.log_message, 
                upstream_host=self.upstream_host
            )
            
            # The TCPServer must be created inside this thread's run method
            self.httpd = socketserver.TCPServer(("", self.port), HandlerWithLogging)
            self.log_message.emit(f"Starting proxy on port {self.port}, forwarding to {self.upstream_host}...")
            self.httpd.serve_forever()
            self.log_message.emit("Proxy server stopped.")
        except Exception as e:
            self.log_message.emit(f"[FATAL] Could not start proxy server: {e}")

    def stop(self):
        """Stops the running proxy server."""
        if self.httpd:
            self.log_message.emit("Shutting down proxy server...")
            self.httpd.shutdown()  # Stop the serve_forever() loop
            self.httpd.server_close()
            self.httpd = None
        self.quit() # End the thread's event loop
        self.wait() # Wait for the thread to finish
