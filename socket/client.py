import socket
import sys
import time
from time import sleep



HOSTNAME = '192.168.0.110'
PORT = 5555
INTERVAL = 1
RETRYTIMES = 3


def socket_connect(host, port, interval, retries):
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for _ in range(retries):
        try:
            c_socket.connect((host, port))
            return c_socket
        except socket.error:
            print("wait"+str(interval)+"s")
            time.sleep(interval)

    c_socket.close()
    return None


def main():
    s = socket_connect(HOSTNAME, PORT, INTERVAL, RETRYTIMES)
    if s is None:
        print("system exit:connection error")
        sys.exit(0)
    while True:
        try:
            data = s.recv(1024).decode()
            if data == "":
                print("server closed")
                break
            print(data)
            sleep(0.2)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(str(e))
            sys.exit(0)



if __name__ == "__main__":
    main()