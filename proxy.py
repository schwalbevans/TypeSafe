import http.server
import socketserver
import requests

# --- Configuration ---
# The target AI service you want to proxy to.
# We'll start with OpenAI's API endpoint.
UPSTREAM_HOST = "https://api.openai.com"
# The port your proxy server will listen on.
PROXY_PORT = 8080

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
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
        Forwards the incoming request to the UPSTREAM_HOST.
        """
        # Construct the full upstream URL
        upstream_url = f"{UPSTREAM_HOST}{self.path}"
        
        # Read the request body if it exists
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Copy headers from the original request, but remove 'Host'
        # as it will be set by the `requests` library.
        headers = {key: value for key, value in self.headers.items() if key.lower() != 'host'}

        try:
            # Make the request to the upstream server
            response = requests.request(
                method,
                upstream_url,
                headers=headers,
                data=body,
                stream=True,  # Use stream to handle large responses efficiently
                timeout=30    # Set a timeout for the upstream request
            )

            # --- Send Response Back to Client ---
            
            # 1. Send status code
            self.send_response(response.status_code)

            # 2. Send headers
            for key, value in response.headers.items():
                # Skip certain headers that can cause issues
                if key.lower() not in ('transfer-encoding', 'content-encoding', 'connection'):
                    self.send_header(key, value)
            self.end_headers()

            # 3. Send the response body
            # Here is where you would intercept and scan the response content.
            # For now, we just forward it.
            if response.content:
                self.wfile.write(response.content)

        except requests.exceptions.RequestException as e:
            # Handle errors (e.g., upstream server is down)
            self.send_error(502, f"Proxy error: {e}")

def run_proxy():
    """
    Starts the reverse proxy server.
    """
    with socketserver.TCPServer(('', PROXY_PORT), ProxyHandler) as httpd:
        print(f"Starting reverse proxy on port {PROXY_PORT}...")
        print(f"Forwarding requests to: {UPSTREAM_HOST}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down proxy server.")
            httpd.server_close()

if __name__ == "__main__":
    run_proxy()
