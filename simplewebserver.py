# -------------------------------------------
#
#
#
# -------------------------------------------


from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import argparse
import re
import cgi

class LocalData(object):
    records = {}

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
            #ctype, pdict = cgi.parse_header(self.headers.get_header('content-type'))
            #print(ctype)

        ctype = self.headers.get_all('content-type')[0]
        length = int(self.headers.get_all('content-length')[0])
        print('ctype = ',ctype)
        print('length = ', length)

        if ctype == 'application/json':
            
            # process request
            data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            print(data)
            recordID = self.path.split('/')[-1]
            LocalData.records[recordID] = data
            print("record $s is added successfully", recordID)
            
            # do response
            self.send_response(200)
            self.send_header('Content-Type', 'application/')
            self.end_headers()

        else:
            data = {}

            self.send_response(200)
            self.end_headers()

        return

    def do_GET(self):
        if None is not re.search('/api/v1/getrecord/*', self.path):
            recordID = self.path.split('/')[-1]
            
            if recordID in LocalData.records:
                self.send_response(200)
                self.send_header('Content-Type')
                self.end_headers()
                self.wfile.write(LocalData.records[recordID])
            else:
                self.send_response(400, 'Bad Request: record does not exist.')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)

class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def addRecord(self, recordID, jsonEncodedRecord):
        LocalData.records[recordID] = jsonEncodedRecord

    def stop(self):
        self.server.shutdown()
        self.waitForThread()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()

    server = SimpleHttpServer(args.ip, args.port)
    print('HTPP Server Running..........')
    server.start()
    server.waitForThread()