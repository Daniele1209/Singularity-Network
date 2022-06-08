from Chain import Chain
from Wallet.Wallet import Wallet
from P2P.SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI

from Exceptions import TransactionValidationError
from Message import Message
import Utils


class Node:
    def __init__(self, ip, port, keyfile):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.keyfile = keyfile

        self.blockchain = Chain()

        """
        Default test accounts for chain transafers
            2 wallets that hold 100 currency
            1 exchange account with 0 balance
        """
        # Initializer for the test wallet
        self.wallet = Wallet()

    def get_wallet(self):
        return self.wallet

    def get_blockchain(self):
        return self.blockchain

    def handle_transaction(self, transaction):
        self.blockchain.insert_transaction(transaction)
        message = Message(self.p2p.socketConnector, "TRANSACTION", transaction)
        # Encode the message
        message_encoded = Utils.encode(message)
        # Broadcast the encoded message
        self.p2p.broadcast(message_encoded)
        # Check if a new forger is required
        if self.blockchain.forger_required():
            self.forge_block()

    # notifies the blockchain that is time to forge a new block
    def forge_block(self):
        chosen_forger = self.blockchain.choose_forger()
        # check if our node is the forger
        if chosen_forger == self.wallet.get_public_key():
            print("I am the chosen forger")
        else:
            print("I suck cock for gold coin !")

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, api_port):
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(api_port)
