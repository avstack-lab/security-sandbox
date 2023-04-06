import socket
import numpy as np
from socket_utils import recv_msg


def main():
    # Set up the socket
    HOST = "127.0.0.1"
    PORT = 4001

    # Send the data
    n_chan = 4
    send_rate = 10  # Hz
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = recv_msg(s)
            A = np.frombuffer(data)
            A = np.reshape(A, (-1, n_chan))
            print(f"Received data of shape {A.shape} at client")


if __name__ == "__main__":
    main()