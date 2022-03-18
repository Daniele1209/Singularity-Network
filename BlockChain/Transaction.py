import copy
import hashlib
import time

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

    def get_fee(self):
        return self._fee

    def signed(self):
        if self._signature:
            return True
        else:
            return False

    def sign_transaction(self, signature):
        self._signature = signature

    def toString(self):
        return str(self._amount) + " " + str(self._payer) + " " + str(self._payee) + " " + str(self._time)

    def payload(self):
        json_representation = copy.deepcopy(self.toJson())
        json_representation['signature'] = ''
        return json_representation

    @staticmethod
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