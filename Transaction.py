import hashlib

class Transaction:

    def __init__(self):
        self._amount = 0
        self._payer = None
        self._payee = None

    def toString(self):
        return str(self._amount) + " " + self._payer + " " + self._payee
