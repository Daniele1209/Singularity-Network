import unittest
from BlockChain.Exceptions import (
    TransactionValidationError,
    BlockValidationError,
    BlockProcessingError,
    AccountModelError
)
from BlockChain.Chain import Chain
from BlockChain.Block import Block
from BlockChain.Transaction import Transaction
from BlockChain.Wallet.Wallet import Wallet
from BlockChain.Config import genesis_dev_address, block_size, minimum_fee


class MyChainTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyChainTester, self).__init__(*args, **kwargs)
        self.test_forger = Wallet(name='forger', write=False)
        self.test_wallet_1 = Wallet(name='test1', write=False)
        self.test_wallet_2 = Wallet(name='test2', write=False)

    def reset_wallets(self):
        self.test_forger = Wallet(name='forger', write=False)
        self.test_wallet_1 = Wallet(name='test1', write=False)
        self.test_wallet_2 = Wallet(name='test2', write=False)

    def chain_with_wallets(self):
        test_chain = Chain()
        test_chain.insert_account(self.test_wallet_1.get_public_key())
        test_chain.insert_account(self.test_wallet_2.get_public_key())
        test_chain.account_model.balance_update(self.test_wallet_1.get_public_key(), 100)
        test_chain.account_model.balance_update(self.test_wallet_2.get_public_key(), 100)
        return test_chain

    def create_valid_transactions(self):
        transaction1 = self.test_wallet_1.createTransaction(10, self.test_wallet_2.get_public_key(), 0.1 * 10)
        transaction2 = self.test_wallet_2.createTransaction(20, self.test_wallet_1.get_public_key(), 0.1 * 20)
        transaction3 = self.test_wallet_1.createTransaction(30, self.test_wallet_2.get_public_key(), 0.1 * 30)
        return [transaction1, transaction2, transaction3]

    def test_genesis(self):
        test_chain = Chain()
        genesis_block = Block(index=0, previousHash=0, transactions=[Transaction(1, "Genesis", "Viniele", 0)],
                              forger=genesis_dev_address)
        genesis_from_chain = test_chain._last_block
        self.assertEqual(genesis_block.toJson(), genesis_from_chain.toJson())
        del test_chain

    def test_add_valid_block(self):
        test_chain = self.chain_with_wallets()
        transactions = self.create_valid_transactions()
        block = self.test_forger.createBlock(test_chain.last_index() + 1, transactions, test_chain._last_block.getHash)
        self.assertTrue(test_chain.push_block(block))
        self.reset_wallets()
        del test_chain

    def test_add_invalid_block(self):
        pass

    """
    def test_add_valid_transaction(self):
        pass

    def test_add_invalid_transaction(self):
        pass

    def test_add_signature_block(self):
        pass

    def test_add_signature_transaction(self):
        pass

    def test_insert_account(self):
        pass

    def test_remove_transactions(self):
        pass

    def test_process_block(self):
        pass

    def test_execute_transactions(self):
        pass

    def test_unsigned_transactions(self):
        pass

    def test_block_validation(self):
        pass

    def test_transaction_validation(self):
        pass
    """


if __name__ == '__main__':
    unittest.main()
