from http.server import *
import argparse
import requests
import socket



'''
Implementation notes:

basic implementation -- act as a proxy(pass thru), when request comes in, fetch/download content from origin server and send it back to client
    - my port range: 20380-20389

    - ssh into the http server
        `ssh -i ssh-ed25519-quach.l.priv quach.l@cdn-http3.khoury.northeastern.edu`
        
    - upload the httpserver.py file to the server
        `scp -i ssh/ssh-ed25519-quach.l.priv httpserver.py quach.l@cdn-http3.khoury.northeastern.edu:~/`
        
    - run http server
        `python3 httpserver.py -p 20380 -o cs5700cdnorigin.ccs.neu.edu`
        
    - curl command to test the HTTP server
        curl http://cs5700cdnorigin.ccs.neu.edu:8080

    - check if server is running
        `time wget http://45.33.55.171:20380/cs5700cdn.example.com`??
        `time wget http://cdn-http3.khoury.northeastern.edu:20380/cs5700cdn.example.com

'''

ORIGIN_SERVER = 'cs5700cdnorigin.ccs.neu.edu' 
ORIGIN_SERVER_PORT = 8080

# basic implementation of proxy server (pass thru)
class HTTPRequestHandler(BaseHTTPRequestHandler):
    cache_content = {}

    def do_GET(self):
        '''
        Handles GET requests, fetches data from origin server & sends it back to client.
        '''
        # for path `/grading/beacon` return 204 status code
        if self.path == '/grading/beacon':
            self.send_response(204)
            self.end_headers()
            return

        # fetch data from origin server
        try:
            response = requests.get(f'http://{ORIGIN_SERVER}:{ORIGIN_SERVER_PORT}{self.path}')
            print(f' ** RESPONSE: {response}, from ORIGIN SERVER: {ORIGIN_SERVER}:{ORIGIN_SERVER_PORT}, for PATH: {self.path} ** ')
            # TODO: cache content

            # send response status code
            self.send_response(response.status_code)
            print(f' ** response STATUS CODE: {response.status_code} ** ')

            # forwards headers from origin server to client
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()

            # send fetched response data/content to client
            self.wfile.write(response.content)
            print(f' ** response CONTENT: {response.content} ** ')
        except requests.exceptions.RequestException as e:
            self.send_error(502, 'Failed to fetch data from origin server')
            print(f' ** ERROR: {e} ** ')


def run_http_server(port, origin_server):
    '''
    Runs the HTTP server.
    '''
    # set origin server url for handler class
    HTTPRequestHandler.origin_server = origin_server
    server_address = ('', port)

    # create server socket
    http_server = HTTPServer(server_address, HTTPRequestHandler)
    print(f' ** http server running on port {port} ** ')
    http_server.serve_forever()


def parse_args():
    '''
    Parses command line arguments.
    '''
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('-p', '--port', required=True, type=int, help='Port number to bind HTTP server to')
    parser.add_argument('-o', '--origin', required=True, type=str, help='Name of origin server for CDN')
    return parser.parse_args()


def main():
    args = parse_args()
    run_http_server(args.port, args.origin)


if __name__ == '__main__':
    main()

