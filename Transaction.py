import hashlib
import time

class Transaction:

    def __init__(self, amount, payer, payee):
        self._amount = amount
        self._payer = payer
        self._payee = payee
        self._time = time.localtime()

    def toString(self):
        return str(self._amount) + " " + str(self._payer) + " " + str(self._payee) + " " + str(self._time)
