from __future__ import annotations

import json
from typing import List, TYPE_CHECKING

from overrides import overrides
from p2pnetwork.node import Node

from BlockChain.Utils import decode
from .PeerDiscoveryHandler import PeerDiscoveryHandler
from .SocketConnector import SocketConnector

if TYPE_CHECKING:
    from BlockChain.Node import Node as SingularityNode
    from BlockChain.P2P.Message import Message


class SocketCommunication(Node):
    peers: List[SocketConnector]
    peerDiscoveryHandler: PeerDiscoveryHandler
    socketConnector: SocketConnector
    node: SingularityNode

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)

    # Open the port
    def start_socket_communication(self, node: SingularityNode, ip: str, port: int):
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.__connect_origin_node(ip, port)

    @overrides
    def inbound_node_connected(self, node):
        self.peerDiscoveryHandler.handshake(node)

    @overrides
    def outbound_node_connected(self, node):
        self.peerDiscoveryHandler.handshake(node)

    def __connect_origin_node(self, ip: str, port: int):
        if (
            self.socketConnector.get_ip() != ip
            or self.socketConnector.get_port() != port
        ):
            self.connect_with_node(ip, port)

    @overrides
    def node_message(self, node, data):
        message: Message = decode(json.dumps(data))
        if message.message_type == "DISCOVERY":
            self.peerDiscoveryHandler.handle_message(message)
        elif message.message_type == "TRANSACTION":
            transaction = message.data
            self.node.handle_transaction(transaction)
        elif message.message_type == "BLOCK":
            block = message.data
            self.node.handle_block(block)
        elif message.message_type == "BLOCKCHAINREQUEST":
            self.node.handle_chain_request(node)
        elif message.message_type == "BLOCKCHAIN":
            blockchain = message.data
            self.node.handle_received_blockchain(blockchain)

    def send(self, receiver, data):
        self.send_to_node(receiver, data)

    def broadcast(self, message):
        self.send_to_nodes(message)
