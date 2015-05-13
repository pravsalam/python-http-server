import urlparse
import BaseHTTPServer
import json
import os
import random
class httpstandardserver(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):
		print(self.headers)
		(client_ip, client_port)=self.client_address
                self.send_response(200)
                self.end_headers()
                self.wfile.write(client_ip)

from BaseHTTPServer import HTTPServer
server = HTTPServer(('',80),httpstandardserver)
print(" Starting http server")
try:
        server.serve_forever()
except KeyboardInterrupt:
        pass
server.server_close()

