from Wallet.Wallet import Wallet
from Chain import Chain
from Node import Node
import Utils

import binascii
from Crypto.PublicKey import RSA
import pem

import requests


def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(
        amount, receiver.get_public_key(), 0.1 * amount, type=type
    )
    url = "http://localhost:5000/transaction"
    package = {"transaction": Utils.encode(transaction)}
    print(package)
    response = requests.post(url, json=package)
    print(response.status_code)


if __name__ == "__main__":

    wallet1 = Wallet(name="wallet1", write=False)
    wallet2 = Wallet(name="wallet2", write=False)
    exchange = Wallet(name="exchange", write=False)

    wallet2.generateFromPair("../Keys/PublicKey.pem", "../Keys/PrivateKey.pem")

    postTransaction(exchange, wallet2, 100, "EXCHANGE")
    postTransaction(exchange, wallet1, 100, "EXCHANGE")
    postTransaction(exchange, wallet1, 10, "EXCHANGE")

    postTransaction(wallet1, wallet1, 25, "STAKE")
    postTransaction(wallet2, wallet1, 10, "TRANSFER")
    postTransaction(wallet2, wallet1, 10, "TRANSFER")
