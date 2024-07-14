import http.server
import socketserver
import cgi

PORT = 2020

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        form_file = form['file']
        
        if form_file.filename:
            with open(form_file.filename, 'wb') as f:
                f.write(form_file.file.read())
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File uploaded successfully!')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'No file uploaded!')
            
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
