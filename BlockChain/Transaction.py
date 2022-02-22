import hashlib
import time

class Transaction:

    def __init__(self, amount, payer, payee, fee):
        self._amount = amount
        self._payer = payer
        self._payee = payee
        self._fee = fee
        self._signature = None
        self._time = time.localtime()

    def signed(self):
        if self._signature:
            return True
        else:
            return False



    def toString(self):
        return str(self._amount) + " " + str(self._payer) + " " + str(self._payee) + " " + str(self._time)
