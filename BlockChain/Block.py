import binascii
import time
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import copy
import Utils as Utl


class Block:
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
        StringToBlock = "{}{}{}{}{}".format(
            self._index,
            self._previousHash,
            self._timeStamp,
            self._forger,
            [tr.toString() for tr in self._transactions],
        )
        return hashlib.sha256(StringToBlock.encode()).hexdigest()

    def get_transactions(self) -> list:
        return self._transactions

    def sign_block(self, signature):
        self._signature = signature

    """
    Verifies with a public key from whom the data came that it was indeed 
    signed by their private key
    param: public_key_loc Path to public key
    param: signature String signature to be verified
    """

    @staticmethod
    def check_verified(data, signature, public_key):
        signature = bytes.fromhex(signature)
        data_hash = Utl.hash(data)
        publicKey = RSA.importKey(public_key)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)
        if signatureSchemeObject.verify(data_hash, signature):
            return True
        return False

    def payload(self):
        json_representation = copy.deepcopy(self.toJson())
        json_representation["signature"] = ""
        return json_representation

    def toJson(self):
        transactions = []
        for trans in self._transactions:
            transactions.append(trans.toJson())

        data = {}
        data["index"] = self._index
        data["previousHash"] = self._previousHash
        data["transactions"] = transactions
        data["timeStamp"] = self._timeStamp
        data["forger"] = self._forger
        data["signature"] = self._signature
        return data

    @staticmethod
    def equals(self, block):
        if self.toJson() == block.toJson():
            return True
        return False

    def __repr__(self) -> str:
        return "{} - {} - {} - {}".format(
            self._index,
            self._previousHash,
            self._transactions.__repr__(),
            self._timeStamp,
        )
