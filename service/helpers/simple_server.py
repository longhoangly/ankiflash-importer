#!/usr/bin/python
# -*- coding: utf-8 -*-

"""A simple HTTP server with REST and json for python 3.
addrecord takes utf8-encoded URL parameters
getrecord returns utf8-encoded json.

Note: this script is cloned from https://gist.github.com/dfrankow/f91aefd683ece8e696c26e183d696c29
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import cgi
import json
import threading
import logging

from . common import *


HOST = "localhost"
PORT = 8081

server = None


class LocalData(object):
    records = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_OPTIONS(self):
        if re.search('/api/v1/addrecord/*', self.path):
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods',
                             'GET, OPTIONS, POST')
            self.send_header("Access-Control-Allow-Headers",
                             "X-Requested-With")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

    def do_POST(self):
        if re.search('/api/v1/addrecord/*', self.path):
            ctype, pdict = cgi.parse_header(
                self.headers.get('content-type'))

            if ctype == 'application/json':
                length = int(self.headers.get('content-length'))
                data = self.rfile.read(length).decode('utf8')
                record_id = self.path.split('/')[-1]

                LocalData.records[record_id] = data
                logging.info("addrecord %s: %s" % (record_id, data[0:100]))

                # HTTP 200: ok
                self.send_response(200)

                # Response data
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                data = json.dumps({"isSuccess": True})
                self.wfile.write(data.encode('utf8'))
            else:
                # HTTP 400: bad request
                self.send_response(400, "Bad Request: must give data")
        else:
            # HTTP 403: forbidden
            self.send_response(403)
        self.end_headers()

    def do_GET(self):
        if re.search('/api/v1/shutdown', self.path):
            # Must shutdown in another thread or we'll hang
            def kill_me_please():
                logging.info("shutdown...")
                self.server.shutdown()

            threading.Thread(target=kill_me_please).start()
            self.server.server_close()
            wait_until(is_port_free(HOST, PORT), 10)

            # Send out a 200 before we go
            self.send_response(200)

        elif re.search('/api/v1/getrecord/*', self.path):
            logging.info("LocalData.records.keys={}".format(
                LocalData.records.keys()))
            record_id = self.path.split('/')[-1]
            if record_id in LocalData.records:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                # Return json, even though it came in as POST URL params
                data = json.dumps(LocalData.records[record_id])
                logging.info("getrecord %s: %s" % (record_id, data[0:100]))
                self.wfile.write(data.encode('utf8'))
            else:
                self.send_response(404, 'Not Found: record does not exist')
        else:
            self.send_response(403)
        self.end_headers()


def init_server(ip, port):
    LocalData.records = {}
    server = HTTPServer((ip, port), HTTPRequestHandler)
    server.serve_forever()
    logging.info('HTTP Server Is STOPPED Running !!!')


def start_server() -> threading.Thread:
    th = threading.Thread(target=init_server, args=(HOST, PORT))
    th.start()

    logging.info('HTTP Server Is Running !!!')
    wait_until(not is_port_free(HOST, PORT), 10)
    return th
