from http.server import BaseHTTPRequestHandler, HTTPServer
from auth import OAuth, Secret 
import re

class Server(BaseHTTPRequestHandler):
    oauth = OAuth()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Twitch stream live</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        pattern = "(\?code=)+"
        ret = re.search(pattern, self.path)
        self.wfile.write(bytes("<p>Regex search pattern %s: %s</p>" % (pattern, "true" if ret else "false"), "utf-8"))
        if(ret):
            self.oauth.set_code(self.path.split("=")[1].split("&")[0])
            self.oauth.twitch_auth_flow()
        else:
            self.oauth.set_query_params("user:read:follows") 
            query = self.oauth.get_query_params()
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes(f"<a href=\"https://id.twitch.tv/oauth2/authorize?{query}\">Connect with Twitch</a>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        
def create_server():
    hostname = "localhost"
    port = 3000
    server = HTTPServer((hostname, port), Server)
    oauth = OAuth()
    user_token = oauth._get_token().user_token
    if(user_token):
        print(f"Token founded! {user_token}\n")
    else:
        print("Please authenticate to get user token access.")
        print("Server started: http://%s:%s" % (hostname, port))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
        print("Closing server connection")

create_server()
