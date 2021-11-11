import socket
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--precentage', type=int,required=True)
    args = parser.parse_args()
    server_address = (args.host, args.port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    message = str(args.precentage)
    sock.sendall(message.encode())

