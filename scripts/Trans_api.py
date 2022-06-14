import os

print(os.getcwd())

import requests

import BlockChain.Utils
from BlockChain.AdditionalTypes import TRANSACTION_TYPE
from BlockChain.Wallet.Wallet import Wallet


def post_transaction(
    sender: Wallet, receiver: Wallet, amount: int, trans_type: TRANSACTION_TYPE
):
    transaction = sender.createTransaction(
        amount, receiver.get_public_key(), 0.1 * amount, type=trans_type
    )
    url = "http://localhost:5000/transaction"
    package = {"transaction": BlockChain.Utils.encode(transaction)}
    print(package)
    response = requests.post(url, json=package)
    print(response.status_code)


if __name__ == "__main__":
    wallet1 = Wallet(name="wallet1", write=False)
    wallet2 = Wallet(name="wallet2", write=False)
    exchange = Wallet(name="exchange", write=False)

    wallet2.generateFromPair("./Keys/PublicKey.pem", "./Keys/PrivateKey.pem")

    post_transaction(exchange, wallet2, 100, "EXCHANGE")
    post_transaction(exchange, wallet1, 100, "EXCHANGE")
    post_transaction(exchange, wallet1, 10, "EXCHANGE")

    post_transaction(wallet1, wallet1, 25, "STAKE")
    post_transaction(wallet2, wallet1, 10, "TRANSFER")
    post_transaction(wallet2, wallet1, 10, "TRANSFER")
