from Chain import Chain
from Wallet.Wallet import Wallet
from P2P.SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI

from Exceptions import TransactionValidationError
from Message import Message
import Utils


class Node:
    def __init__(self, ip, port):
        self.p2p = None
        self.ip = ip
        self.port = port

        self.blockchain = Chain()

        """
        Default test accounts for chain transafers
            2 wallets that hold 100 currency
            1 exchange account with 0 balance
        """
        self.test_exchange = Wallet(name="exchange", write=True)
        self.test_wallet_1 = Wallet(name="test1", write=True)
        self.test_wallet_2 = Wallet(name="test2", write=True)
        self.blockchain.insert_account(self.test_exchange.get_public_key())
        self.blockchain.insert_account(self.test_wallet_1.get_public_key())
        self.blockchain.insert_account(self.test_wallet_2.get_public_key())
        self.blockchain.account_model.balance_update(
            self.test_wallet_1.get_public_key(), 100
        )
        self.blockchain.account_model.balance_update(
            self.test_wallet_2.get_public_key(), 100
        )

        # Initializer for the test wallet
        self.wallet = Wallet()

    def get_wallet(self):
        return self.wallet

    def get_blockchain(self):
        return self.blockchain

    def handle_transaction(self, transaction):
        try:
            self.blockchain.insert_transaction(transaction)
            message = Message(self.p2p.socketConnector, "TRANSACTION", transaction)
            # Encode the message
            message_encoded = Utils.encode(message)
            # Broadcast the encoded message
            self.p2p.broadcast(message_encoded)
            # Check if a new forger is required
            if self.blockchain.forger_required():
                self.forge_block()

        except TransactionValidationError:
            pass

    # notifies the blockchain that is time to forge a new block
    def forge_block(self):
        

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, api_port):
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(api_port)
