import os
import argparse
import time
import yaml

import avsec



def create_lidar_attacker(attacker_config):
    with open(attacker_config, 'r') as f:
        config = yaml.safe_load(f)
    if config["attacker"] == "FalsePositiveObjectAttacker":
        attacker = avsec.attack.lidar.attacker.FalsePositiveObjectAttacker(
            awareness=config["awareness"], framerate=config["framerate"], dataset=config["dataset"])
    else:
        raise NotImplementedError(config["attacker"])
    return attacker


class RunnableAttacker():
    def __init__(self, attacker) -> None:
        self.attacker = attacker

    def poll(self):
        pass

    def close(self):
        pass


def main(args):
    if not os.path.exists(args.attacker_config):
        raise FileNotFoundError(f'Cannot find attacker config at {args.attacker_config}')
    attacker = create_lidar_attacker(args.attacker_config)
    runnable = RunnableAttacker(attacker)
    try:
        while True:
            runnable.poll()
            time.sleep(0.01)
    except:
        runnable.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("attacker_config", type=str)

    args = parser.parse_args()
    main(args)