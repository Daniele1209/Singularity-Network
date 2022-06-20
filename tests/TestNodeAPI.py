import unittest

import requests

import BlockChain.Utils as Utls
from BlockChain.Chain import Chain
from BlockChain.Node import Node
from BlockChain.Wallet.Wallet import Wallet
from BlockChain.NodeAPI import NodeAPI


class MyNodeAPITester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MyNodeAPITester, self).__init__(*args, **kwargs)
        self.test_forger = Wallet(name="forger", write=False)
        self.test_wallet_1 = Wallet(name="test1", write=False)
        self.test_wallet_2 = Wallet(name="test2", write=False)

        self.ip = "localhost"
        self.port = 6969
        self.api_port = 4200

    def reset_wallets(self):
        self.test_forger = Wallet(name="forger", write=False)
        self.test_wallet_1 = Wallet(name="test1", write=False)
        self.test_wallet_2 = Wallet(name="test2", write=False)

    def chain_with_wallets(self):
        test_chain = Chain()
        test_chain.insert_account(self.test_forger.get_public_key())
        test_chain.insert_account(self.test_wallet_1.get_public_key())
        test_chain.insert_account(self.test_wallet_2.get_public_key())
        test_chain.account_model.balance_update(
            self.test_wallet_1.get_public_key(), 100
        )
        test_chain.account_model.balance_update(
            self.test_wallet_2.get_public_key(), 100
        )
        return test_chain

    def create_node_instance(self):
        node = Node(self.ip, self.port)
        node.startP2P()
        nodeApi = NodeAPI(node)
        nodeApi.start("localhost", self.api_port)
        return node, nodeApi

    def test_create_valid_transaction(self):
        node, nodeApi = self.create_node_instance()
        transaction = self.test_wallet_1.createTransaction(
            10, self.test_wallet_2.get_public_key(), 0.1 * 10
        )

        url = "http://localhost:4200/transaction"
        package = {"transaction": Utls.encode(transaction)}
        request = requests.post(url, json=package)
        print(request.text)


if __name__ == "__main__":
    unittest.main()
