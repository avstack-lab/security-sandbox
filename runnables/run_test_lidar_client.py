import argparse
import socket
import time

import numpy as np
from socket_utils import recv_msg, send_msg


def main(args):
    # Send the data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.host, args.port))
        while True:
            # -- receive
            data = recv_msg(s)
            A = np.reshape(np.frombuffer(data), (-1, args.n_channels))
            print(f"Received data at client")

            # -- send
            time.sleep(0.01)  # processing time
            send_msg(s, A.tobytes())
            print(f"Sent data from the client")


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
