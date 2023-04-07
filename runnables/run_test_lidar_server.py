import argparse
import socket
import time

import numpy as np
from socket_utils import recv_msg, send_msg


def main(args):
    # Send the data
    send_rate = 10  # Hz
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((args.host, args.port))
        s.listen()
        print(f"Waiting for client connection...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected to by {addr}")
            while True:
                # -- send
                n_pts = np.random.randint(low=30000, high=40000)
                A = np.random.randn(n_pts, args.n_channels)
                send_msg(conn, A.tobytes())
                print(f"Sent data from server")

                # -- receive
                data = recv_msg(conn)
                A2 = np.reshape(np.frombuffer(data), (-1, args.n_channels))
                print(f"Received data at the server")
                time.sleep(1.0 / send_rate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost", type=str)
    parser.add_argument("--port", default=3000, type=int)
    parser.add_argument(
        "--n_channels",
        default=4,
        type=int,
        choices=[3, 4, 5],
        help="Number of point cloud channels (columns)",
    )

    args = parser.parse_args()
    main(args)
