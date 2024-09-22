"""



"""

import os
import threading
from rsshub import create_app
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("--ip", type=str, default="127.0.0.1")
parser.add_argument("--port", type=str, default=5005)
parser.add_argument("--https", action="store_true")
parser.add_argument("--debug", action="store_true")
parser.add_argument("--feeder", action="store_true")
args = parser.parse_args()


def main():
    if args.feeder:
        print("enabled feeder, lets feeder!")
        from rsshub.rssfeeder.rss import start_feeds_scheduler

        feeds_thread = threading.Thread(target=start_feeds_scheduler)
        feeds_thread.start()

    app = create_app("production")
    app.run(host=args.ip, port=args.port, debug=args.debug)
