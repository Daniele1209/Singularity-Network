#from Crypto import Random
#from Crypto.PublicKey import RSA
import hashlib
from Transaction import *

class Wallet:

    def __init__(self, public, private):
        self._publicKey = public
        self._privateKey = private
        self.generateKeyPair()

    # We use "RSA" encryption - use to encypt and decrypt
    # Use public key to encrypt
    # Use private key to decrypt
    # => we use both keys to create a digital signature
    # Sign the hash with the private key, so the message can be verified using the public key
    def generateKeyPair(self):
        pass

    def storePair(self):
        pass

    def sendMoney(self, amount, payeePublicKey):
        executedTransaction = Transaction(amount, self._publicKey, payeePublicKey)
        sign = hashlib.sha256()
        sign.update(executedTransaction.toString()).hexdigest()


print(r"""
███████╗██╗███╗   ██╗ ██████╗ ██╗   ██╗██╗      █████╗ ██████╗ ██╗████████╗██╗   ██╗ ██████╗ ██████╗ ██╗███╗   ██╗
██╔════╝██║████╗  ██║██╔════╝ ██║   ██║██║     ██╔══██╗██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝██╔════╝██╔═══██╗██║████╗  ██║
███████╗██║██╔██╗ ██║██║  ███╗██║   ██║██║     ███████║██████╔╝██║   ██║    ╚████╔╝ ██║     ██║   ██║██║██╔██╗ ██║
╚════██║██║██║╚██╗██║██║   ██║██║   ██║██║     ██╔══██║██╔══██╗██║   ██║     ╚██╔╝  ██║     ██║   ██║██║██║╚██╗██║
███████║██║██║ ╚████║╚██████╔╝╚██████╔╝███████╗██║  ██║██║  ██║██║   ██║      ██║   ╚██████╗╚██████╔╝██║██║ ╚████║
╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝
""")
