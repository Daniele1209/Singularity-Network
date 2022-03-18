from hashlib import sha256

import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii

from ecdsa import SECP256k1

import Utils

from BlockChain.Block import Block
from BlockChain.Transaction import Transaction
from base64 import b64encode
from ecdsa.keys import SigningKey


class Wallet():

    def __init__(self, name='#', write=True):
        self.key_signature = SigningKey.generate(
            curve=SECP256k1, hashfunc=sha256
        )
        self._publicKey = None
        self._privateKey = None
        self._name = name
        self.write = write
        self.generateKeyPair()

    def get_public_key(self):
        return self._publicKey

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

        if self.write:
            file_out = open("Keys/" + self._name + "_PrivateKey.pem", "wb")
            file_out.write(private_key.export_key())
            file_out = open("Keys/" + self._name + "_PublicKey.pem", "wb")
            file_out.write(public_key.export_key())

        self._privateKey = key_pair["private_key"]
        self._publicKey = key_pair["public_key"]

    def createBlock(self, index, transactions, lastHash):
        block = Block(index, lastHash, transactions, self._publicKey)
        signature = self.sign(block.payload())
        block.sign_block(signature)
        return block

    def createTransaction(self, amount, receiver, fee, type='TRANSFER'):
        transaction = Transaction(amount, self._publicKey, receiver, fee, type)
        signature = self.sign(transaction.payload())
        transaction.sign_transaction(signature)
        return transaction

    def sign(self, data):
        hash_data = Utils.hash(data)
        private_key_rsa = RSA.importKey(binascii.unhexlify(self._privateKey))
        signature_object = PKCS1_v1_5.new(private_key_rsa)
        signature = signature_object.sign(hash_data)
        return signature.hex()

    def toJson(self):
        return self.__dict__
