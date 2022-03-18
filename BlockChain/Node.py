from BlockChain.Chain import Chain
from BlockChain.Wallet.Wallet import Wallet

class Node():
    def __init__(self):
        self.blockchain = Chain()
        self.wallet = Wallet(blockchain=self.blockchain)

    def get_wallet(self):
        return self.wallet

    def get_blockchain(self):
        return self.blockchain
