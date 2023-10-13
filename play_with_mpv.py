#!/usr/bin/env python
# Plays MPV when instructed to by a chrome extension =]

import sys
import argparse
from subprocess import Popen

FileNotFoundError = IOError
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
            urls = str(query["play_url"][0])
            if urls.startswith('magnet:') or urls.endswith('.torrent'):
                try:
                    pipe = Popen(['peerflix', '-k',  urls, '--', '--force-window'] +
                                 query.get("mpv_args", []))
                except FileNotFoundError as e:
                    missing_bin('peerflix')
            else:
                try:
                    pipe = Popen(['mpv', urls, '--force-window'] +
                                 query.get("mpv_args", []))
                except FileNotFoundError as e:
                    missing_bin('mpv')
            self.respond(200, "playing...")
        elif "cast_url" in query:
            urls = str(query["cast_url"][0])
            if urls.startswith('magnet:') or urls.endswith('.torrent'):
                print(" === WARNING: Casting torrents not yet fully supported!")
                try:
                    with Popen(['mkchromecast', '--video',
                                '--source-url', 'http://localhost:8888']):
                        pass
                except FileNotFoundError as e:
                    missing_bin('mkchromecast')
                pipe.terminate()
            else:
                try:
                    pipe = Popen(['mkchromecast', '--video', '-y', urls])
                except FileNotFoundError as e:
                    missing_bin('mkchromecast')
            self.respond(200, "casting...")

        elif "fairuse_url" in query:
            urls = str(query["fairuse_url"][0])
            location = query.get("location", ['~/Downloads/'])[0]
            if "%" not in location:
                location += "%(title)s.%(ext)s"
            print("downloading ", urls, "to", location)
            if urls.startswith('magnet:') or urls.endswith('.torrent'):
                msg = " === ERROR: Downloading torrents not yet supported!"
                print(msg)
                self.respond(400, msg)
            else:
                try:
                    pipe = Popen(['youtube-dl', urls, '-o', location] +
                                 query.get('ytdl_args', []))
                except FileNotFoundError as e:
                    missing_bin('youtube-dl')
                self.respond(200, "downloading...")
        else:
            self.respond(400)


def missing_bin(bin):
    print("======================")
    print("ERROR: "+bin.upper()+" does not appear to be installed correctly!")
    print("please ensure you can launch '"+bin+"' in the terminal.")
    print("======================")


def start():
    parser = argparse.ArgumentParser(description='Plays MPV when instructed to by a browser extension.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port',   type=int,  default=7531, help='The port to listen on.')
    parser.add_argument('--public', action='store_true',     help='Accept traffic from other computers.')
    args = parser.parse_args()
    hostname = '0.0.0.0' if args.public else 'localhost'
    httpd = BaseHTTPServer.HTTPServer((hostname, args.port), Handler)
    print("serving on {}:{}".format(hostname, args.port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" shutting down...")
        httpd.shutdown()


if __name__ == '__main__':
    start()

