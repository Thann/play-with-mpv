#!/bin/env python
import sys
from subprocess import Popen

if sys.version_info[0] < 3:  # python 2
    import BaseHTTPServer
else:  # python 3
    import http.server as BaseHTTPServer

PORT = 7531

if sys.version_info[0] < 3:
    class CompatibilityMixin:
        def send_body(self, msg):
            self.wfile.write(msg+'\n')
            self.wfile.close()
else:
    class CompatibilityMixin:
        def send_body(self, msg):
            self.wfile.write(bytes(msg+'\n', 'utf-8'))


class Handler(BaseHTTPServer.BaseHTTPRequestHandler, CompatibilityMixin):
    def respond(self, code, body=None):
        self.send_response(code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        if body:
            self.send_body(body)

    def do_GET(self):
        url = self.path.split("?",1)[1].split("=",1)
        print(url)
        if url[0] == "play_url":
            url = url[1]
            if url.startswith('magnet:') or url.endswith('.torrent'):
                pipe = Popen(['peerflix', '-k',  url, '--', '--force-window'])
            else:
                pipe = Popen(['mpv', url, '--force-window'])
            self.respond(200, "playing...")
        else:
            self.respond(400)


def start():
    httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
    print("serving at port {}".format(PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" shutting down...")
        httpd.shutdown()


if __name__ == '__main__':
    start()

