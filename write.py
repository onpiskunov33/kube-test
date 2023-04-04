from http.server import HTTPServer, BaseHTTPRequestHandler
import socket, psycopg2, os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Version: ' + version.encode())
        self.wfile.write(b'\nHello world from hostname: ' + socket.gethostname().encode() + b'\n')
        if "favicon" not in self.path:
            date = self.date_time_string()
            hostname = socket.gethostname()
            self.wfile.write(b'\n hostname ->  ' + hostname.encode())
            self.wfile.write(b'\n Date -> ' + date.encode())
            print(f'hostname ->  {hostname}, Date -> {date}')
            con = psycopg2.connect(
                database = os.environ['POSTGRES_DB'],
                user = os.environ['POSTGRES_USER'],
                password = os.environ['POSTGRES_PASSWORD'],
                host = "postgres-service", 
                port = "5432"
            )
            print("Database opened successfully")
            cur = con.cursor()  
            cur.execute(
                "INSERT INTO access (versionn, date_time, hostname) VALUES (%s, %s, %s)", (version, date, hostname)
            )
            con.commit()  
            print("Record inserted successfully")
            self.wfile.write(b"\n\nRecord inserted successfully")
            con.close()


SERVER_PORT = 8000
version = "latest"
print('Version:', version)
httpd = HTTPServer(('0.0.0.0', SERVER_PORT), SimpleHTTPRequestHandler)
print('Listening on port %s ...' % SERVER_PORT)
httpd.serve_forever()