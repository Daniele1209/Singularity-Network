import threading
import time

from config import settings

import BlockChain.Utils as Utls
from BlockChain.AdditionalTypes import MESSAGE_TYPE
from .Message import Message


# Sub-module of Socket Communication
# Frequently connect to the whole network to see if there are new nodes
# Broadcasts all the nodes he knows to the network
class PeerDiscoveryHandler:
    def __init__(self, node):
        self.socketCommunication = node

    def discovery(self):
        while True:
            handshakeMessage = self.handshake_message()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(settings.delay_between_p2p_network_discovery_seconds)

    def status(self):
        while True:
            print("Current connections: ")
            for peer in self.socketCommunication.peers:
                print(f"ip: {peer.ip} | port: {peer.port}")
            time.sleep(settings.delay_between_p2p_network_discovery_seconds)

    # start discovery and status in their own thread
    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        discoveryThread = threading.Thread(target=self.discovery, args=())
        statusThread.start()
        discoveryThread.start()

    # Exchange information between the nodes
    def handshake(self, node):
        handshake_message_send = self.handshake_message()
        self.socketCommunication.send(node, handshake_message_send)

    def handshake_message(self):
        socket_connector = self.socketCommunication.socketConnector
        peers = self.socketCommunication.peers
        data = peers
        message_type: MESSAGE_TYPE = "DISCOVERY"
        message = Message(socket_connector, message_type, data)

        encoded_message = Utls.encode(message)
        return encoded_message

    def handle_message(self, message):
        peer_socketConnector = message.sender_connector
        peer_list = message.data
        new_peer = True

        for peer in self.socketCommunication.peers:
            if peer.equals(peer_socketConnector):
                new_peer = False

        # if peer is new, add it to list of peers
        if new_peer:
            self.socketCommunication.peers.append(peer_socketConnector)

        # if there are new peers, we should connect to them
        for peersPeer in peer_list:
            peer_known = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peer_known = True
            if not peer_known and not peersPeer.equals(
                self.socketCommunication.socketConnector
            ):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)
