#!/usr/bin/env python

"""
Publishes software updates to listeners.
"""

import zmq
from newest.state import State

class Server:
    def __init__(self):
        self.software_state = State()

        self.ctx = zmq.Context.instance()
        self.poller = zmq.Poller()

        # socket for receiving update notifications
        self.sub_socket = self.ctx.socket(zmq.PULL)
        self.sub_socket.bind('tcp://*:5558')
        self.poller.register(self.sub_socket, zmq.POLLIN)

    def handle_update(self):
        json = self.sub_socket.recv()
        new_state = State.deserialize(json)
        # FIXME do some sanity checks instead of just overwriting
        self.software_state.software_versions = {**self.software_state.software_versions, **new_state.software_versions}
        print("update received:")
        print(str(self.software_state))

    def main_loop(self):
        while True:
            items = dict(self.poller.poll(1000))
            if self.sub_socket in items:
                self.handle_update()

def main():
    server = Server()
    server.main_loop()

if __name__ == "__main__":
    main()
