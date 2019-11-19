import http.server as httpsrvr
import socketserver as socketsrvr

if __name__ == '__main__':

    Handler = httpsrvr.SimpleHTTPRequestHandler
    PORT = 8080
    while True:
        try:
            httpd = socketsrvr.TCPServer(("", PORT), Handler)
            break
        except:
            continue

    print("serving at port %d" % PORT)
    httpd.serve_forever()
