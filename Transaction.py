import hashlib

class Transaction:

    def __init__(self, amount, payer, payee):
        self._amount = amount
        self._payer = payer
        self._payee = payee

    def toString(self):
        return str(self._amount) + " " + self._payer + " " + self._payee
