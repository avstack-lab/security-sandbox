import time
import socket
import numpy as np
from socket_utils import send_msg, recv_msg


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
            # -- receive
            data = recv_msg(s)
            A = np.reshape(np.frombuffer(data), (-1, n_chan))
            print(f"Received data at client")

            # -- send
            time.sleep(0.01)  # processing time
            send_msg(s, A.tobytes())
            print(f"Sent data from the client")

if __name__ == "__main__":
    main()