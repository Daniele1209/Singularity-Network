from p2pnetwork.node import Node
import json

from P2P.SocketConnector import SocketConnector
from P2P.PeerDiscoveryHandler import PeerDiscoveryHandler
from P2P.SocketConnector import SocketConnector
import Utils as Utls

class SocketCommunication(Node):

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)

    # Open the port
    def startSocketCommunication(self):
        self.start()
        self.peerDiscoveryHandler.start()
        self.connect_originNode()

    def inbound_node_connected(self, node):
        self.peerDiscoveryHandler.handshake(node)

    def outbound_node_connected(self, node):
        self.peerDiscoveryHandler.handshake(node)

    def connect_originNode(self):
        if self.socketConnector != 10001:
            self.connect_with_node('localhost', 10001)

    def node_message(self, node, data):
        message = Utls.decode(json.dumps(data))
        if message.message_type == 'DISCOVERY':
            self.peerDiscoveryHandler.handle_message(message)

    def send(self, receiver, data):
        self.send_to_node(receiver, data)

    def broadcast(self, message):
        self.send_to_nodes(message)