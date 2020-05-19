import socket
import sys
import time
from time import sleep


HOSTNAME = '192.168.0.110'
PORT = 5000


def main():
    print("waiting connect...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOSTNAME, PORT))
    s.listen(1)
    connect, address = s.accept()
    print(connect)
    print(address)
    while True:
        try:
            result = predict()
            connect.send(result)
            print("sent result data")
            sleep(0.2)
        except KeyboardInterrupt:
            s.close()
            break
        except Exception as e:
            print(str(e))
            sys.exit(0)


def predict():
    result = "1".encode()
    return result

if __name__ == "__main__":
    main()