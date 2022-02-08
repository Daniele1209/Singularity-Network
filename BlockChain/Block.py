import time
import hashlib
import math
import random
from hashlib import sha256
from  ecdsa.keys import VerifyingKey, BadSignatureError
from ecdsa.curves import SECP256k1
from base64 import b64decode

class Block:

    def __init__(self, index, previousHash, transactions: list, forger, signature=None):
        self._index = index
        self._previousHash = previousHash
        self._transactions = transactions
        self._timeStamp = time.time()
        self._forger = forger
        self._signature = signature
        # used for the proof of work system
        self._nonce = math.floor(random.random() * 999999999)

    """
    Hash built using the block parameters
    """
    @property
    def getHash(self) -> object:
        StringToBlock = "{}{}{}".format(self._index, self._previousHash, self._timeStamp)
        return hashlib.sha256(StringToBlock.encode()).hexdigest()

    @property
    def nonce(self) -> object:
        return self._nonce

    def get_nonce(self) -> object:
        return self._nonce

    def sign_block(self, signature):
        self._signature = signature

    """
    Check if the signature is verified or not
    return True if it is and False otherwise
    """
    @staticmethod
    def check_verified(self) -> bool:
        key_to_verify = VerifyingKey.from_string(b64decode(self._forger), curve=SECP256k1, hashfunc=sha256)
        try:
            key_to_verify.verify(b64decode(self._signature), self.getHash(), hashfunc=sha256)
        except BadSignatureError:
            return False
        return True

    def __repr__(self) -> str:
        return "{} - {} - {} - {}".format(self._index, self._previousHash, self._transactions, self._timeStamp)


