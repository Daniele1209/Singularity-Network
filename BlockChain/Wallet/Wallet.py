import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii
import sys

from Utils import hash, encode, decode

from Block import Block
from Transaction import Transaction


class Wallet:
    def __init__(self, name="#", write=True):
        self._key_pair = None
        self._publicKey = None
        self._privateKey = None
        self._name = name
        self.write = write
        self.generateKeyPair()

    def get_public_key(self):
        return self._publicKey

    def get_publicKey_string(self):
        return self._publicKey

    def set_name(self, new_name):
        self._name = new_name

    # Generate wallet based on key pair
    def generateFromPair(self, file_public, file_private):
        with open(file_public, "r") as public_file:
            public_key = RSA.importKey(public_file.read())

        with open(file_private, "r") as private_file:
            private_key = RSA.importKey(private_file.read())
        try:
            self._publicKey = public_key.exportKey("PEM").decode("utf-8")
            self._privateKey = private_key.exportKey("PEM").decode("utf-8")
        except:
            raise Exception("Wallet key import filed !")

    # We use "RSA" encryption - use to encrypt and decrypt
    # Use public key to encrypt
    # Use private key to decrypt
    # => we use both keys to create a digital signature
    # Sign the hash with the private key, so the message can be verified using the public key
    def generateKeyPair(self):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(2048, random_gen)
        self._key_pair = private_key
        public_key = private_key.publickey()
        key_pair = {
            "private_key": private_key.exportKey("PEM").decode("utf-8"),
            "public_key": public_key.exportKey("PEM").decode("utf-8"),
        }

        if self.write:
            file_out = open("../Keys/" + self._name + "_PrivateKey.pem", "wb")
            file_out.write(private_key.export_key())
            file_out = open("../Keys/" + self._name + "_PublicKey.pem", "wb")
            file_out.write(public_key.export_key())

        self._privateKey = key_pair["private_key"]
        self._publicKey = key_pair["public_key"]

    def createBlock(self, index, transactions, lastHash):
        block = Block(index, lastHash, transactions, self._publicKey)
        signature = self.sign(block.payload())
        block.sign_block(signature)
        return block

    def createTransaction(self, amount, receiver, fee, type="TRANSFER"):
        transaction = Transaction(
            amount, self.get_publicKey_string(), receiver, fee, type
        )
        signature = self.sign(transaction.payload())
        transaction.sign_transaction(signature)
        return transaction

    def sign(self, data):
        hash_data = hash(data)
        private_key_rsa = RSA.importKey(self._privateKey)
        signature_object = PKCS1_v1_5.new(private_key_rsa)
        signature = signature_object.sign(hash_data)
        return signature.hex()

    """
    Verifies with a public key from whom the data came that it was indeed 
    signed by their private key
    param: public_key_loc Path to public key
    param: signature String signature to be verified
    """

    @staticmethod
    def check_verified(data, signature, public_key):
        signature = bytes.fromhex(signature)
        data_hash = hash(data)
        publicKey = RSA.importKey(binascii.unhexlify(public_key))
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)
        if signatureSchemeObject.verify(data_hash, signature):
            return True
        return False
