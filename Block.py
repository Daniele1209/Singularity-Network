import time
import hashlib

class Block:

    def __init__(self, index, proof, previousHash, transaction):
        self._index = index
        self._proof = proof
        self._previousHash = previousHash
        self._transaction = transaction
        self._timeStamp = time.time()

    @property
    def getHash(self):
        StringToBlock = "{}{}{}{}{}".format(self._index, self._previousHash, self._transaction, self._transaction, self._timeStamp)
        return hashlib.sha256(StringToBlock.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self._index, self._previousHash, self._transaction, self._transaction, self._timeStamp)