from Chain import Chain
from Wallet.Wallet import Wallet
from P2P.SocketCommunication import SocketCommunication

class Node():
    def __init__(self, ip, port):
        self.p2p = None
        self.ip = ip
        self.port = port

        self.blockchain = Chain()
        self.wallet = Wallet()

    def get_wallet(self):
        return self.wallet

    def get_blockchain(self):
        return self.blockchain

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication()
