import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
import binascii
import hashlib
from Transaction import Transaction

class Wallet:

    def __init__(self, chain):
        self._publicKey = None
        self._privateKey = None
        self.generateKeyPair()
        self._Chain = chain

    # We use "RSA" encryption - use to encypt and decrypt
    # Use public key to encrypt
    # Use private key to decrypt
    # => we use both keys to create a digital signature
    # Sign the hash with the private key, so the message can be verified using the public key
    def generateKeyPair(self):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(2048, random_gen)
        public_key = private_key.publickey()
        key_pair = {
		    "private_key" : binascii.hexlify(private_key.exportKey(format='PEM')).decode('ascii'),
		    "public_key": binascii.hexlify(public_key.exportKey(format='PEM')).decode('ascii')
	    }

        self._privateKey = key_pair["private_key"]
        self._publicKey = key_pair["public_key"]

    def sendCoins(self, amount, payeePublicKey):
        executedTransaction = Transaction(amount, self._publicKey, payeePublicKey)

        private_key = RSA.importKey(binascii.unhexlify(self._privateKey))
        signer = PKCS1_v1_5.new(private_key)
        hash = SHA.new(executedTransaction.toString().encode('utf8'))
        signature = binascii.hexlify(signer.sign(hash)).decode('ascii')

        self._Chain.addBlock(self._publicKey, signature, executedTransaction)