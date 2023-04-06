import time
import socket
import numpy as np
from socket_utils import send_msg


def main():
    # Set up the socket
    HOST = "localhost"
    PORT = 4001

    # Send the data
    n_chan = 4
    send_rate = 10  # Hz
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Waiting for client connection...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected to by {addr}")
            while True:
                n_pts = np.random.randint(low=30000, high=40000)
                A = np.random.randn(n_pts, n_chan)
                send_msg(conn, A.tobytes())
                print(f"Sent data of shape {A.shape} from server")
                time.sleep(1./send_rate)


if __name__ == "__main__":
    main()