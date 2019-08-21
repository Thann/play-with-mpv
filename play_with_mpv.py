#!/usr/bin/env python
# Plays MPV when instructed to by a chrome extension =]

import sys
from subprocess import Popen
PORT = 7531

if sys.version_info[0] < 3:  # python 2
    import BaseHTTPServer
    import urlparse
    class CompatibilityMixin:
        def send_body(self, msg):
            self.wfile.write(msg+'\n')
            self.wfile.close()

else:  # python 3
    import http.server as BaseHTTPServer
    import urllib.parse as urlparse
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
        try:
            url = urlparse.urlparse(self.path)
            query = urlparse.parse_qs(url.query)
        except:
            query = {}
        if query.get('mpv_args'):
            print("MPV ARGS:", query.get('mpv_args'))
        if "play_url" in query:
            url = query["play_url"][0]
            if url.startswith('magnet:') or url.endswith('.torrent'):
                pipe = Popen(['peerflix', '-k',  url, '--', '--force-window'] +
                             query.get("mpv_args", []))
            else:
                pipe = Popen(['mpv', url, '--force-window'] +
                             query.get("mpv_args", []))
            self.respond(200, "playing...")
        elif "cast_url" in query:
            url = query["cast_url"][0]
            if url.startswith('magnet:') or url.endswith('.torrent'):
                print(" === WARNING: Casting torrents not yet fully supported!")
                with Popen(['mkchromecast', '--video',
                            '--source-url', 'http://localhost:8888']):
                    pass
                pipe.terminate()
            else:
                pipe = Popen(['mkchromecast', '--video', '-y', url])
            self.respond(200, "casting...")

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

