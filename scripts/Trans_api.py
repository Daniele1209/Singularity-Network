import BlockChain.Utils
import requests
from BlockChain.AdditionalTypes import TRANSACTION_TYPE
from BlockChain.Wallet.Wallet import Wallet
from config import settings
import time


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
    """
    Default test accounts for chain transfers
        2 wallets that hold 100 currency
        1 exchange account with 0 balance
    """
    wallet1 = Wallet(name="wallet1", write=False)
    wallet2 = Wallet(name="wallet2", write=False)
    exchange = Wallet(
        name="exchange", write=False
    )  # why is this the exchange account since wallet2 has genesis key

    exchange.generateFromPair(
        "../Keys/exchange_PublicKey.pem", "../Keys/exchange_PrivateKey.pem"
    )
    wallet2.generateFromPair(
        "../Keys/test2_PublicKey.pem", "../Keys/test2_PrivateKey.pem"
    )
    wallet1.generateFromPair(
        "../Keys/test1_PublicKey.pem", "../Keys/test1_PrivateKey.pem"
    )

    post_transaction(exchange, wallet2, 100, "EXCHANGE")
    post_transaction(exchange, wallet1, 100, "EXCHANGE")
    post_transaction(exchange, wallet1, 10, "EXCHANGE")

    time.sleep(3)

    post_transaction(wallet1, wallet1, 25, "STAKE")
    post_transaction(wallet2, wallet1, 10, "TRANSFER")
    post_transaction(wallet2, wallet1, 10, "TRANSFER")

    time.sleep(3)

    # changes the forger to wallet 1
    post_transaction(wallet1, wallet2, 50, "TRANSFER")
    post_transaction(wallet2, wallet1, 40, "TRANSFER")
    post_transaction(wallet1, wallet2, 30, "TRANSFER")
