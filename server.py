from http.server import BaseHTTPRequestHandler, HTTPServer
from utils import get_client_id

CLIENT_ID = get_client_id()

class Server(BaseHTTPRequestHandler):
    query = f'response_type=code&client_id={CLIENT_ID}&redirect_uri=http://localhost:3000&scope=user:read:follows'
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Twitch stream live</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(f"<a href=\"https://id.twitch.tv/oauth2/authorize?{self.query}\">Connect with Twitch</a>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        
def create_server():
    hostname = "localhost"
    port = 3000
    server = HTTPServer((hostname, port), Server)
    print(server.path)
    print("Server started: http://%s:%s" % (hostname, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Closing server connection")

create_server()
