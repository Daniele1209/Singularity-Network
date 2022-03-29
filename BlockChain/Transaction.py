import binascii
import copy
import time

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import Utils


class Transaction:

    # type can be STAKING or TRANSFER
    def __init__(self, amount, payer, payee, fee, type='TRANSFER'):
        self._amount = amount
        self._payer = payer
        self._payee = payee
        self._fee = fee
        self._type = type
        self._signature = None
        self._time = time.localtime()

    def get_payer(self):
        return self._payer

    def get_payee(self):
        return self._payee

    def get_amount(self):
        return self._amount

    def get_signature(self):
        return self._signature

    def get_fee(self):
        return self._fee

    def signed(self):
        if self._signature:
            return True
        else:
            return False

    def sign_transaction(self, signature):
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
        data_hash = Utils.hash(data)
        publicKey = RSA.importKey(binascii.unhexlify(public_key))
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)
        if signatureSchemeObject.verify(data_hash, signature):
            return True
        return False


    def toString(self):
        return str(self._amount) + " " + str(self._payer) + " " + str(self._payee) + " " + str(self._time)

    def payload(self):
        json_representation = copy.deepcopy(self.toJson())
        json_representation['signature'] = ''
        return json_representation

    def equals(self, transaction):
        if transaction.toJson() == self.toJson():
            return True
        return False

    def toJson(self):
        data = {}
        data['amount'] = self._amount
        data['payer'] = self._payer
        data['payee'] = self._payee
        data['fee'] = self._fee
        data['type'] = self._type
        data['time'] = self._time
        data['signature'] = self._signature
        return data