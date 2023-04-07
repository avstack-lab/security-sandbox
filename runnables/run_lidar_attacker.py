import argparse
import os
import socket
import time

import avsec
import numpy as np
import yaml
from socket_utils import recv_msg, send_msg


def create_lidar_attacker(attacker_config):
    with open(attacker_config, "r") as f:
        config = yaml.safe_load(f)
    if config["attacker"] == "FalsePositiveObjectAttacker":
        attacker = avsec.attack.lidar.attacker.FalsePositiveObjectAttacker(
            awareness=config["awareness"],
            framerate=config["framerate"],
            dataset=config["dataset"],
        )
    elif config["attacker"] == "PassthroughAttacker":
        attacker = avsec.attack.lidar.attacker.PassthroughAttacker(
            dataset=config["dataset"]
        )
    else:
        raise NotImplementedError(config["attacker"])
    return attacker


class RunnableAttacker:
    def __init__(self, attacker, sock, HOST, PORT, BIND=True, n_channels=4) -> None:
        self.attacker = attacker
        self.HOST = HOST
        self.PORT = PORT
        self.BIND = BIND
        self.sock = sock
        self.sock.connect((args.host, args.port))
        self.n_channels = n_channels

    def poll(self):
        # -- wait for receive
        data = recv_msg(self.sock)
        PC = np.reshape(np.frombuffer(data), (-1, self.n_channels))
        print("Received point cloud!")

        # -- perform processing
        PC, info, diagnostics = self.attacker(PC)

        # -- send back result
        send_msg(self.sock, PC.tobytes())
        print("Sent point cloud!")

    def close(self):
        pass  # no need to do anything


def main(args):
    if not os.path.exists(args.attacker_config):
        raise FileNotFoundError(
            f"Cannot find attacker config at {args.attacker_config}"
        )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        attacker = create_lidar_attacker(args.attacker_config)
        runnable = RunnableAttacker(
            attacker, sock, args.host, args.port, n_channels=args.n_channels
        )
        try:
            while True:
                runnable.poll()
                time.sleep(0.01)
        except Exception as e:
            runnable.close()
            raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("attacker_config", type=str)
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
