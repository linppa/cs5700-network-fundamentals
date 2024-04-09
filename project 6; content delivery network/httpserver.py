from http.server import *
import socketserver
import urllib.request
import os
import threading

'''
Implementation notes:
    - my port range: 20380-20389

    - ssh into the http server
        `ssh -i ssh-ed25519-quach.l.priv quach.l@cdn-http3.khoury.northeastern.edu`
        
    - upload the httpserver.py file to the server
        `scp -i ssh/ssh-ed25519-quach.l.priv httpserver.py quach.l@cdn-http3.khoury.northeastern.edu:~/`
        
    - run http server
        `python3 httpserver.py -p 8080 -o http://cs5700cdnorigin.ccs.neu.edu:8080/`

'''
# server name & IP address of HTTP cache servers, TODO: check if correct IP
REPLICA_SERVERS = {
    'cdn-http3.khoury.northeastern.edu': '45.33.55.171',
    'cdn-http4.khoury.northeastern.edu': '170.187.142.220', 
    'cdn-http7.khoury.northeastern.edu': '213.168.249.157', 
    'cdn-http11.khoury.northeastern.edu': '139.162.82.207', 
    'cdn-http14.khoury.northeastern.edu': '45.79.124.209', 
    'cdn-http15.khoury.northeastern.edu': '192.53.123.145', 
    'cdn-http16.khoury.northeastern.edu': '192.46.221.203',
}

CACHE_DATA = {}
ORIGIN_SERVER = 'http://cs5700cdnproject.ccs.neu.edu:8080'

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        Handles GET requests.
        '''
        # check if data is in cache
        if self.path in CACHE_DATA:
            print(f' ** data found in cache for path: {self.path} ** ')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(CACHE_DATA[self.path])
            print(' ** CACHE DATA: {CACHE_DATA} ** ')
            return
        
        # get data from origin server
        elif self.path not in CACHE_DATA:
            print(f' ** data not found in cache for path: {self.path} ** ')
            print(f' ** fetching data from origin server: {ORIGIN_SERVER} ** ')
            try:
                response = urllib.request.urlopen(f'{ORIGIN_SERVER}{self.path}')
                html_data = response.read()
                CACHE_DATA[self.path] = html_data
                print(f' ** data added to cache for path: {self.path} ** ')

                # send response to client
                self.send_response(200)
                self.send_header('Content-type', 'text/html') # TODO: check if this is correct
                self.end_headers()
                self.wfile.write(html_data)
                print(' ** CACHE DATA: {CACHE_DATA} ** ')
                return
            except Exception as e:
                print(f' ** error with http request handler: {e} ** ')
                self.send_error(404, f'error with http request handler: {e}')
        
        # TODO: handle errors


def run_http_server(port):
    '''
    Runs the HTTP server.
    '''
    # create server socket
    server = HTTPServer(('localhost', port), HTTPRequestHandler)
    print(f' ** http server running on port {port} ** ')
    server.serve_forever()

if __name__ == '__main__':
    run_http_server(8080)

