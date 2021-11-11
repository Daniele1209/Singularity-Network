import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
from hashlib import sha256
import binascii
import hashlib
from Transaction import Transaction


class Wallet:

    def __init__(self, chain):
        self._publicKey = None
        self._privateKey = None
        self.generateKeyPair()
        self._Chain = chain
        self._coin_count = 100

    # We use "RSA" encryption - use to encrypt and decrypt
    # Use public key to encrypt
    # Use private key to decrypt
    # => we use both keys to create a digital signature
    # Sign the hash with the private key, so the message can be verified using the public key
    def generateKeyPair(self):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(2048, random_gen)
        public_key = private_key.publickey()
        key_pair = {
            "private_key": binascii.hexlify(private_key.exportKey(format='PEM')).decode('ascii'),
            "public_key": binascii.hexlify(public_key.exportKey(format='PEM')).decode('ascii')
        }

        file_out = open("PrivateKey.pem", "wb")
        file_out.write(private_key.export_key())
        file_out = open("PublicKey.pem", "wb")
        file_out.write(public_key.export_key())

        self._privateKey = key_pair["private_key"]
        self._publicKey = key_pair["public_key"]

    def sendCoins(self, amount, payeePublicKey):
        if self._coin_count - amount >= 0:
            executedTransaction = Transaction(amount, self._publicKey, payeePublicKey)

            private_key = RSA.importKey(binascii.unhexlify(self._privateKey))
            signer = PKCS1_v1_5.new(private_key)
            _hash = SHA.new(executedTransaction.toString().encode('utf8'))
            signature = binascii.hexlify(signer.sign(_hash)).decode('ascii')

            self._Chain.addBlock(self._publicKey, signature, executedTransaction)
            self._coin_count -= amount
        else:
            raise binascii.Error("Insufficient balance !")

    def get_public_key(self):
        return self._publicKey

    def get_coins(self):
        return self._coin_count
