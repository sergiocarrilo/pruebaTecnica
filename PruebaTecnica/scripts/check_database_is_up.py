import socket
import  time
import argparse



parser = argparse.ArgumentParser(description='Check if database port is up')

parser.add_argument('--ip', required=True)
parser.add_argument('--port', required=True)

args = parser.parse_args()

ip = str(args.ip)
port = int(args.port)

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print("Database is up")
        break
    print("Database is not up, checking soon")
    time.sleep(5)
