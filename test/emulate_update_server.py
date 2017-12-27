
# A simple download server for testing osnap.  Emulates github LFS, but all the storage is local so we don't
# use github server space.

import json
import threading
import glob
import os
import re
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

account_name = 'jamesabel'
project_name = 'osnaptest'

dft_local_host = 'http://localhost'


def get_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


class EmulatorBaseHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text')  # no html, just text
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def wfile_write(self, return_message):
        print(self.path)
        self.wfile.write(return_message.encode())


class HashAndSizeHTTPRequestHandler(EmulatorBaseHTTPRequestHandler):
    """
    emulate:
    get latest version hash and size:
    https://raw.githubusercontent.com/jamesabel/osnaptest/master/installers/osnaptest_installer.exe

    version https://git-lfs.github.com/spec/v1
    oid sha256:a079104ddcda2f11f654ba48fe4046d202c7e002373ffcefb47b7f6a1c645dfb
    size 114765708
    """
    def do_GET(self):
        self._set_headers()
        return_message = None
        supported_path = '%s/%s/master' % (account_name, project_name)
        if self.path[1:].startswith(supported_path):
            # get the local file path
            file_path = self.path[1:].replace(supported_path, '')[1:].replace('/', os.sep)
            if os.path.exists(file_path):
                return_lines = ['version https://git-lfs.github.com/spec/v1',
                                'oid sha256:%s' % get_sha256(file_path),
                                'size %d' % os.path.getsize(file_path)]
                return_message = '\n'.join(return_lines)
        if return_message is None:
            self.send_response(404)
            return_message = json.dumps({'not found': self.path, 'expected': supported_path})
        self.wfile_write(return_message)


class TagsHTTPRequestHandler(EmulatorBaseHTTPRequestHandler):
    def do_GET(self):
        self._set_headers()
        supported_path = 'repos/%s/%s/tags' % (account_name, project_name)
        if self.path[1:] == supported_path:
            """
            emulate relevant part of:
            https://api.github.com/repos/jamesabel/osnaptest/tags
            """
            tags = []
            # get the latest update .zip version in the local installers dir
            for zip_file_path in glob.glob(os.path.join('installers', '*.zip')):
                search_results = re.search('(_update_)([0-9.]+)(.zip)', zip_file_path)
                if search_results:
                    tags.append({'name': search_results.group(2)})
            return_message = json.dumps(tags, indent=4)
        else:
            self.send_response(404)
            return_message = json.dumps({'not found': self.path, 'expected': supported_path})
        self.wfile_write(return_message)


class EmulateServer(threading.Thread):
    def __init__(self, http_handler_class, port):
        super().__init__()
        self.http_handler_class = http_handler_class
        self.port = port
        self.server = None
        print('%s:%d' % (dft_local_host, self.port))  # not the full URL - add the rest of the path to this

    def run(self):
        server_address = ('', self.port)
        self.server = HTTPServer(server_address, self.http_handler_class)
        self.server.serve_forever()  # call server.shutdown() to exit


def main():
    # pick some random ephemeral ports on which to emulate the servers used for updating
    http_port_base = 55015
    server_threads = [EmulateServer(SimpleHTTPRequestHandler, http_port_base),  # downloader
                      EmulateServer(TagsHTTPRequestHandler, http_port_base+1),
                      EmulateServer(HashAndSizeHTTPRequestHandler, http_port_base+2)]
    for server_thread in server_threads:
        server_thread.start()
    input('press enter to shut down servers')
    for server_thread in server_threads:
        print('shutting down %s:%d' % (dft_local_host, server_thread.port))
        server_thread.server.shutdown()


if __name__ == "__main__":
    main()
