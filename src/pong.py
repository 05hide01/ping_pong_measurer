from typing import Any, Iterator
import logging
import time

import zenoh
# from zenoh.session import Session, Sample

class Pong():
    def __init__(self, 
                 node_id: int, 
                 session: Any, 
                 ) -> None:

        self._node_id = node_id
        # self.session = session : session はpickleできない？
        self._ping_key = "ping_topic" + str(node_id)
        self._pong_key = "pong_topic" + str(node_id)

        self.publisher = session.declare_publisher(self._pong_key)

        self.subscriber = session.declare_subscriber(
            self._ping_key, 
            self.callback
            )

    def callback(self, sample: Any):
        # message = sample.payload.decode('utf-8')
        message = bytes(sample.payload).decode('utf-8')
        self.pong(message)
        # Convert ZBytes to bytes and then decode
        print(f"Received message size: {len(message)}")

    def pong(self, message:str):
        self.publisher.put(message)

    def start(self):
        while True:
            logging.info("pong: serving")
            time.sleep(5)

if __name__ == "__main__":
    import argparse
    import common
    parser = argparse.ArgumentParser(prog="z_pong", description="zenoh get example")
    common.add_config_arguments(parser)
    parser.add_argument(
        "--express",
        dest="express",
        metavar="EXPRESS",
        type=bool,
        default=False,
        help="Express publishing",
    )

    args = parser.parse_args()
    # conf = common.get_config_from_args(args)
    # session = zenoh.open(conf)
    conf = zenoh.Config()
    session = zenoh.open(config=conf)
    pong = Pong(0, session)

    pong.sample()
