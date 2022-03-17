from hashlib import sha256

import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii

from ecdsa import SECP256k1

from BlockChain.Block import Block
from BlockChain.Transaction import Transaction
from base64 import b64encode
from ecdsa.keys import SigningKey


class Wallet:

    def __init__(self, chain, name):
        self.key_signature = SigningKey.generate(
            curve=SECP256k1, hashfunc=sha256
        )
        self._publicKey = None
        self._privateKey = None
        self.generateKeyPair()
        self._Chain = chain
        self._coin_count = 100
        self._name = name

    def get_public_key(self):
        return self._publicKey

    def get_coins(self):
        return self._coin_count

    def set_name(self, new_name):
        self._name = new_name

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

        file_out = open("Keys/" + self._name + "/PrivateKey.pem", "wb")
        file_out.write(private_key.export_key())
        file_out = open("Keys/" + self._name + "/PublicKey.pem", "wb")
        file_out.write(public_key.export_key())

        self._privateKey = key_pair["private_key"]
        self._publicKey = key_pair["public_key"]

    def sendCoins(self, amount, payeePublicKey, fee):
        if self._coin_count - (amount + fee) >= 0:
            executedTransaction = Transaction(amount, self._publicKey, payeePublicKey, fee)

            private_key = RSA.importKey(binascii.unhexlify(self._privateKey))
            signer = PKCS1_v1_5.new(private_key)
            _hash = SHA.new(executedTransaction.toString().encode('utf8'))
            signature = binascii.hexlify(signer.sign(_hash)).decode('ascii')
            self._coin_count -= amount
        else:
            raise binascii.Error("Insufficient balance !")

    def sign(self, hash):
        return b64encode(
            self.key_signature.sign(hash.encode(), hashfunc=sha256)
        ).decode()

    @staticmethod
    def toJson(self):
        return self.__dict__
