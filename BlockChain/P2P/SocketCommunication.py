from p2pnetwork.node import Node
import json

from .SocketConnector import SocketConnector
from .PeerDiscoveryHandler import PeerDiscoveryHandler
from .SocketConnector import SocketConnector
from .Message import Message
import Utils as Utls


class SocketCommunication(Node):
    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)

    # Open the port
    def startSocketCommunication(self, node, ip, port):
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.connect_originNode(ip, port)

    def inbound_node_connected(self, node):
        self.peerDiscoveryHandler.handshake(node)

    def outbound_node_connected(self, node):
        self.peerDiscoveryHandler.handshake(node)

    def connect_originNode(self, ip, port):
        if (
            self.socketConnector.get_ip() != ip
            or self.socketConnector.get_port() != port
        ):
            self.connect_with_node(ip, port)

    def node_message(self, conn_node, data):
        message = Utls.decode(json.dumps(data))
        if message.message_type == "DISCOVERY":
            self.peerDiscoveryHandler.handle_message(message)
        elif message.message_type == "TRANSACTION":
            transaction = message.data
            self.node.handle_transaction(transaction)
        elif message.message_type == "BLOCK":
            block = message.data
            print("\nGOT BLOCK\n")
            print(str(block.toJson()))
            self.node.handle_block(block)
        elif message.message_type == "BLOCKCHAINREQUEST":
            self.node.handle_chain_request(conn_node)
        elif message.message_type == "BLOCKCHAIN":
            blockchain = message.data
            self.node.handle_received_blockchain(blockchain)

    def send(self, receiver, data):
        self.send_to_node(receiver, data)

    def broadcast(self, message):
        self.send_to_nodes(message)
