#!/usr/bin/env -S python3 -u

import argparse, socket, time, json, select, struct, sys, math

DATA_SIZE = 1375

class Sender:
    def __init__(self, host, port):
        self.host = host
        self.remote_port = int(port)
        self.log("Sender starting up using port %s" % self.remote_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 0))
        self.waiting = False

    def log(self, message):
        sys.stderr.write(message + "\n")
        sys.stderr.flush()

    def send(self, message):
        self.socket.sendto(json.dumps(message).encode('utf-8'), (self.host, self.remote_port))

    def run(self):
        while True:
            sockets = [self.socket, sys.stdin] if not self.waiting else [self.socket]

            socks = select.select(sockets, [], [], 0.1)[0]
            for conn in socks:
                if conn == self.socket:
                    k, addr = conn.recvfrom(65535)
                    msg = k.decode('utf-8')

                    self.log("Received message '%s'" % msg)
                    self.waiting = False
                elif conn == sys.stdin:
                    data = sys.stdin.read(DATA_SIZE)
                    if len(data) == 0:
                        self.log("All done!")
                        sys.exit(0)

                    msg = { "type": "msg", "data": data }
                    self.log("Sending message '%s'" % msg)
                    self.send(msg)
                    self.waiting = True

        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='send data')
    parser.add_argument('host', type=str, help="Remote host to connect to")
    parser.add_argument('port', type=int, help="UDP port number to connect to")
    args = parser.parse_args()
    sender = Sender(args.host, args.port)
    sender.run()
