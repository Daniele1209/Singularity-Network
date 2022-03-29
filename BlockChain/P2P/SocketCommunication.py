from p2pnetwork.node import Node
from P2P.PeerDiscoveryHandler import PeerDiscoveryHandler

class SocketCommunication(Node):

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)

    # Open the port
    def startSocketCommunication(self):
        self.start()
        self.peerDiscoveryHandler.start()

    def inbound_node_connected(self, node):
        print('Inbound connection')
        self.send_to_node(node, 'Node you connected to')

    def outbound_node_connected(self, node):
        print('Outbound connection')
        self.send_to_node(node, 'Node who made connection')

    def node_message(self, node, data):
        print(data)