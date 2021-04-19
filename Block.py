import time
import hashlib
import math
import random

class Block:

    def __init__(self, index, proof, previousHash, transaction):
        self._index = index
        self._proof = proof
        self._previousHash = previousHash
        self._transaction = transaction
        self._timeStamp = time.time()
        # used for the proof of work system
        self._nonce = math.floor(random.random() * 999999999)

    @property
    def getHash(self):
        StringToBlock = "{}{}{}{}{}".format(self._index, self._previousHash, self._transaction, self._transaction, self._timeStamp)
        return hashlib.sha256(StringToBlock.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self._index, self._previousHash, self._transaction, self._transaction, self._timeStamp)

    def get_nonce(self):
        return self._nonce

    def get_proof(self):
        return self._proof

    @property
    def nonce(self):
        return self._nonce