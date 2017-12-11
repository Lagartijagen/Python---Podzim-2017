import http.server
import socketserver

PORT = 8000

#Handler = http.server.SimpleHTTPRequestHandler

#with socketserver.TCPServer(("", PORT), Handler) as httpd:
#    print("serving at port", PORT)
#    httpd.serve_forever()


class myHandler(http.server.SimpleHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == '/':
            message = "Work Work!"
        elif self.path == '/file.txt':
            message = "You have requested this useless file. It's misery is broken!"
        self.wfile.write(bytes(message, "utf8"))
        return

try:
    with socketserver.TCPServer(("", PORT), myHandler) as httpd:
        httpd.serve_forever()


except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    httpd.socket.close()