
import time
import threading

# Sub-module of Socket Communication
# Frequently connect to the whole network to see if there are new nodes
# Broadcasts all the nodes he knows to the network
class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socketCommunication = node

    def discovery(self):
        while True:
            print('discovery ...')
            time.sleep(10)

    def status(self):
        while True:
            print('status')
            time.sleep(10)

    # start discovery and status in their own thread
    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        discoveryThread = threading.Thread(target=self.discovery, args=())
        statusThread.start()
        discoveryThread.start()