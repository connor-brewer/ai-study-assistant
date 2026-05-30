"""
OAuth Callback Handler - Simple local server to handle OAuth redirects
"""
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Supabase"""
    
    # Class variable to store the received code
    received_code = None
    received_access_token = None
    received_refresh_token = None
    
    def do_GET(self):
        """Handle GET request from OAuth redirect"""
        # Parse the URL and query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Get the authorization code or tokens from the URL
        if 'code' in query_params:
            OAuthCallbackHandler.received_code = query_params['code'][0]
        
        if 'access_token' in query_params:
            OAuthCallbackHandler.received_access_token = query_params['access_token'][0]
        
        if 'refresh_token' in query_params:
            OAuthCallbackHandler.received_refresh_token = query_params['refresh_token'][0]
        
        # Send success response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        success_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful</title>
            <style>
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #FAFAFA;
                }
                .container {
                    text-align: center;
                    background: white;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                .success-icon {
                    font-size: 64px;
                    margin-bottom: 20px;
                }
                h1 {
                    color: #2C2C2C;
                    margin: 0 0 10px 0;
                }
                p {
                    color: #777777;
                    margin: 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success-icon">✅</div>
                <h1>Authentication Successful!</h1>
                <p>You can close this window and return to the app.</p>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(success_html.encode())
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

def start_callback_server(port=8080, timeout=60):
    """
    Start a temporary HTTP server to handle OAuth callback
    
    Args:
        port: Port to listen on (default 8080)
        timeout: How long to wait for callback in seconds (default 60)
    
    Returns:
        Dict with received tokens/code or None if timeout
    """
    # Reset class variables
    OAuthCallbackHandler.received_code = None
    OAuthCallbackHandler.received_access_token = None
    OAuthCallbackHandler.received_refresh_token = None
    
    server = HTTPServer(('localhost', port), OAuthCallbackHandler)
    
    # Run server in a thread with timeout
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for callback with timeout
    server_thread.join(timeout=timeout)
    
    # Clean up
    server.server_close()
    
    # Return received data
    return {
        'code': OAuthCallbackHandler.received_code,
        'access_token': OAuthCallbackHandler.received_access_token,
        'refresh_token': OAuthCallbackHandler.received_refresh_token
    }

