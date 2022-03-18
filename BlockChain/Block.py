import time
import hashlib
import math
import random
from hashlib import sha256
from ecdsa.keys import VerifyingKey, BadSignatureError
from ecdsa.curves import SECP256k1
from base64 import b64decode
import copy

class Block():

    def __init__(self, index, previousHash, transactions: list, forger, signature=None):
        self._index = index
        self._previousHash = previousHash
        self._transactions = transactions
        self._timeStamp = time.time()
        self._forger = forger
        self._signature = signature

    # Getters
    def get_index(self):
        return self._index

    def get_prevHash(self):
        return self._previousHash

    def get_timeStamp(self):
        return self._timeStamp

    def get_forger(self):
        return self._forger

    def get_signature(self):
        return self._signature

    """
    Hash built using the block parameters
    """
    @property
    def getHash(self) -> object:
        StringToBlock = "{}{}{}{}{}".format(self._index, self._previousHash, self._timeStamp, self._forger,
                                            [tr.toString() for tr in self._transactions])
        return hashlib.sha256(StringToBlock.encode()).hexdigest()

    def get_transactions(self) -> list:
        return self._transactions

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

    def payload(self):
        json_representation = copy.deepcopy(self.toJson())
        json_representation['signature'] = ''
        return json_representation

    def toJson(self):
        data = {}
        data['index'] = self._index
        data['previousHash'] = self._previousHash
        transactions = []
        for trans in self._transactions:
            transactions.append(trans.toJson())
        data['transactions'] = transactions
        data['timeStamp'] = self._timeStamp
        data['forger'] = self._forger
        data['signature'] = self._signature
        return data

    @staticmethod
    def equals(self, block):
        if self.toJson() == block.toJson():
            return True
        return False

    def __repr__(self) -> str:
        return "{} - {} - {} - {}".format(self._index, self._previousHash, self._transactions.__repr__(), self._timeStamp)


