from Block import *
from Transaction import *

class Chain:

    def __init__(self):
        self._chain = []
        self._nodes = set()
        # Defining the first block in the chain
        self.Genesis()
    
    def Genesis(self):
        self.newBlock(0, 0, Transaction(1, "Genesis", "Viniele"))

    def newBlock(self, proof, previousHash, transaction):
        block = Block(len(self._chain), proof, previousHash, transaction)
        self._chain.append(block)

        return block

    @property
    def lastBlock(self):
        return self._chain[-1]

    
