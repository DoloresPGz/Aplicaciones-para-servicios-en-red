import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

values = [ "value0", "value1", "value2", "value3"]


class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()

    # Search
    def do_GET(self):
        print("GET request: \n")
        print(self.path)
        print(self.headers)
        content_len = int(self.headers.get('Content-Length', 0))
        expect = self.headers.get("Connection", False)
        if expect:
            if self.headers.get("Upgrade", False):
                msg = "Upgrade petition accepted to " + self.headers.get("Upgrade")
                self.send_response(101)
                self.send_header("Connection", "Upgrade")
                self.send_header('Content-type', 'text/html')
                self.send_header("Content-Length", len(msg))
                self.send_header("Upgrade", self.headers.get("Upgrade"))
                body = self.rfile.read(0)
                self.end_headers()
                return
        if self.path.endswith("sub-string"):
            string = "This is a string"
            header_range = self.headers.get("Range", "Not found range")
            range = header_range.split("-")

            substring = string[int(range[0]) : int(range[1])]
            if substring:
                self.send_response(206)
                self.send_header("Content-Range", "characters = " + range[0] + "-" + range[1])
                self.send_header("Content-type", "plain/text")
                self.end_headers()
                self.wfile.write(substring.encode())
            else:
                self.send_response(416)
                self.send_header("Content-type", "plain/text")
                self.end_headers()
                self.wfile.write("The range does not match".encode())
            return

        if self.path.endswith("multiple-path"):
            body = "<p>Seleccione una dirección<p>"
            self.send_response(300)
            self.send_header("Access-Control-Allow-Headers", "Content")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Links", "/link2,/link1")
            self.send_header("Conthent-type", "text/html")
            self.send_header("Location", "/link1")
            self.end_headers()
            self.wfile.write(body.encode())
            return

        if  self.path.endswith("moved-path"):
            print("301")
            msg = "<p>This direction has been removed permanently<p>"
            self.send_response(301)
            self.send_header("Location", "http://localhost//new_path")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(msg.encode())
            return

        if  self.path.endswith("moved-path-tem"):
            print("302")
            msg = "<p>This direction has been removed for a while<p>"
            self.send_response(302)
            self.send_header("Location", "http://localhost//new_path_temporal")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(msg.encode())
            return

        if  self.path.endswith("authentication"):
            print("401")
            credential = "1234"
            auto = self.headers.get("Authorization", "")
            if auto:
                if auto == credential:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write("<p>Hello<p>".encode())
                else:
                    self.send_response(401)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write("<p>Incorrect credentials<p>".encode())
            else:
                self.send_response(403)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("<h1>You can't enter here</h1>".encode())
            return

        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<h1>Not found</h1>".encode())
        return

    def do_TRACE(self):
        self.send_response(405)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<h1>Try another method</h1>".encode())
        return

    # Adding new resource
    def do_POST(self):
        print("POST request:\n")
        msg = ""

        ''' Reads post request body '''
        #self._set_headers()
        print(self.path)
        print(self.headers)

        if len(self.path) > 20:
            self.send_response(414)
            self.end_headers()
            return

        if self.path.endswith("large-content"):
            content_len = int(self.headers.get('Content-Length', None))
            expect = self.headers.get("Expect", "")
            if expect:
                if expect == "100-continue":
                    if content_len or content_len != 0:
                        if content_len < 50:
                            # En lugar de un 100, manda un 200
                            self.send_response(200)
                        else :
                            self.send_response(413)
                            msg = "<p> El tamaño del cuerpo de la petición no es aceptado por el servidor </p>"
                    else:
                        self.send_response(411)
                        print("length required")
                else:
                    self.send_response(417)
                    msg = "<p> No identificamos formato: " + expect + "</p>"
                self.end_headers()
            return

        if self.path.endswith("new-request"):
            self.send_response(202)
            self.send_header("Link", "http://localhost//new-request-status")
            self.end_headers()
            return

        if self.path.endswith("new-user"):
            content_len = int(self.headers.get('Content-Length', 0))
            self.send_response(201)
            self.send_header('Last-Modified', self.date_time_string(time.time()))
            self.end_headers()
            if not msg:
                msg = self.rfile.read(content_len)
            print("Post body", msg)
            self.wfile.write("new user request:{}".format(msg).encode())
            return

        if self.path.endswith("new-form"):
            content_len = int(self.headers.get('Content-Length', 0))
            print("new-form")
            #len_body = len(self.headers.get("Content-Length", 0))
            self.send_response(205)
            self.send_header('Last-Modified', self.date_time_string(time.time()))
            self.send_header("Connection", "close")
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            body = self.rfile.read(content_len)
            print("New form:", body)
            return

        if self.path.endswith("see-other"):
            msg = "<p>To see the results, please check our link</p>"
            self.send_response(303)
            self.send_header("Location", "http://localhost//confirmation")
            self.end_headers()
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            print(body)
            self.wfile.write(msg.encode())
            return

        if self.path.endswith("add-image"):
            msg = "<p>We don't support this format</p>"
            image = self.headers.get("Content-type", "")
            if image:
                if image == "image/jpeg":
                    self.send_response(200)
                    body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                    print(body)
                    self.end_headers()
                    return
                else:
                    self.send_response(406)
                    self.end_headers()
                    self.wfile.write(msg.encode())
                    return
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write("<p>Server requires Content-type".encode())
                return

        if self.path.endswith("deleted-folder"):
            msg = "<p>This folder doesn't exist anymore</p>"
            self.send_response(410)
            self.end_headers()
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            print(body)
            self.wfile.write(msg.encode())
            return

        if self.path.endswith("add-user"):
            if self.headers.get("Content-type") == "application/json":
                self.send_response(201)
                self.end_headers()
                body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                print(body)
                return
            else:
                self.send_response(415)
                self.end_headers()

        content_len = int(self.headers.get("Content-Length", 0))
        self.send_response(409)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        body = self.rfile.read(content_len)
        print(body)
        self.wfile.write("<p>You have to create the folder before uploading some data</p>".encode())


    # Add and Update (Idemponent)
    def do_PUT(self):
        self.do_POST()

    # Search head of file
    def do_HEAD(self):
        if self.path.endswith("modified-cons"):
            e_tag = "1234"
            tag = self.headers.get("If-None-Match", "ERROR")
            if e_tag == tag:
                self.send_response(304)
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("ETag", e_tag)
                self.end_headers()
            return

    def do_DELETE(self):
        print("DELETE request:\n")
        if self.path.endswith("user-delete"):
            self.send_response(204)
            self.send_header('Last-Modified', self.date_time_string(time.time()))
            self.end_headers()
            print(self.path)
            print(self.headers)

    def do_CONNECT(self):
        self.send_response(501)
        self.end_headers()
        self.wfile.write("<p>This should have worked, sorry</p>".encode())
'''

    def do_OPTIONS(self):

'''


host = '127.0.0.1'
port = 8081
print("server started working", host, port)
HTTPServer((host, port), HandleRequests).serve_forever()