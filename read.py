from http.server import HTTPServer, BaseHTTPRequestHandler
import socket, psycopg2, os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Version: ' + version.encode())
        self.wfile.write(b'\nHello world from hostname: ' + socket.gethostname().encode() + b'\n\n')
        if "favicon" not in self.path:
            con = psycopg2.connect(
                database = os.environ['POSTGRES_DB'],
                user = os.environ['POSTGRES_USER'],
                password = os.environ['POSTGRES_PASSWORD'],
                host = "postgres-service", 
                port = "5432"
            )
            print("Database opened successfully")
            cur = con.cursor()  
            cur.execute("SELECT id, versionn, date_time, hostname from access")
            rows = cur.fetchall()
            for row in rows:  
                print("ID =", row[0])
                print("Ver =", row[1])
                print("DATE =", row[2])
                print("HOST =", row[3], "\n")
                self.wfile.write(b'ID = ' + str(row[0]).encode())
                self.wfile.write(b' , Ver = ' + row[1].encode())
                self.wfile.write(b' , DATE = ' + row[2].encode())
                self.wfile.write(b' , HOST = ' + row[3].encode() + b'\n')
            print("Operation done successfully")  
            con.close()


SERVER_PORT = 8000
version = "v1"
print('Version:', version)
httpd = HTTPServer(('0.0.0.0', SERVER_PORT), SimpleHTTPRequestHandler)
print('Listening on port %s ...' % SERVER_PORT)
httpd.serve_forever()