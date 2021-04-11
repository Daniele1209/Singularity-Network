import time

from Transaction import *

class Block:

    def __init__(self, previousHash):
        self._previousHash = previousHash
        self._transaction = Transaction
        self.timeStamp = time.time()

    def getHash(self):
        StringToBlock = "{}{}{}".format(self._previousHash, self._transaction, self.timeStamp)
        return hashlib.sha256(StringToBlock.encode()).hexdigest()