import http.server as httpsrvr
import socketserver as socketsrvr

PORT = 8000

Handler = httpsrvr.SimpleHTTPRequestHandler

httpd = socketsrvr.TCPServer(("", PORT), Handler)

print("serving at port")
httpd.serve_forever()