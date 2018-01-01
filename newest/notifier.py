#!/usr/bin/env python

"""
Notifies the server with software updates.
"""

import argparse
import zmq
from newest.state import State

class Notifier:
    def __init__(self):
        self.ctx = zmq.Context.instance()
        self.socket = self.ctx.socket(zmq.PUSH)
        #self.socket.linger = 0
        self.socket.connect('tcp://127.0.0.1:5558')

    def notify(self, name, version):
        state = State()
        state.update(name, version)
        json = state.serialize()
        self.socket.send(json)

def main():
    parser = argparse.ArgumentParser('Send a notfication about a new software version')
    parser.add_argument('name')
    parser.add_argument('version')
    args = parser.parse_args()

    notifier = Notifier()
    notifier.notify(args.name, args.version)

if __name__ == "__main__":
    main()
