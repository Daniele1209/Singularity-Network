from Wallet.Wallet import Wallet
from Chain import Chain
from Node import Node
import Utils

import binascii
from Crypto.PublicKey import RSA
import pem

import requests


def postTransaction(sender, receiver, amount):
    transaction = sender.createTransaction(
        receiver.get_public_key(), amount, 0.1 * amount
    )
    url = "http://localhost:5000/transaction"
    package = {"transaction": Utils.encode(transaction)}
    print(package)
    request = requests.post(url, json=package)


if __name__ == "__main__":
    public_filename = "_PublicKey.pem"
    private_filename = "_PrivateKey.pem"
    key_path = "../Keys/"
    # wallet1 = Wallet(name="wallet1", write=False)
    # wallet2 = Wallet(name="wallet2", write=False)
    # exchange = Wallet(name="exchange", write=False)
    wallet1 = Wallet()
    wallet2 = Wallet()
    wallet1.generateFromPair(
        key_path + "test1" + public_filename, key_path + "test1" + private_filename
    )
    wallet2.generateFromPair(
        key_path + "test2" + public_filename, key_path + "test2" + private_filename
    )
    # forger: genesis
    # postTransaction(exchange, wallet1, 10)
    postTransaction(wallet1, wallet2, 10)
    # postTransaction(exchange, wallet2, 10)
