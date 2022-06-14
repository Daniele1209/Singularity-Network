import binascii
import unittest

from BlockChain.Exceptions import (
    TransactionValidationError,
    BlockValidationError,
    BlockProcessingError,
    AccountModelError,
)
from BlockChain.Chain import Chain
from BlockChain.Block import Block
from BlockChain.Transaction import Transaction
from BlockChain.Wallet.Wallet import Wallet
from config import settings


class MyChainTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MyChainTester, self).__init__(*args, **kwargs)
        self.test_forger = Wallet(name="forger", write=False)
        self.test_wallet_1 = Wallet(name="test1", write=False)
        self.test_wallet_2 = Wallet(name="test2", write=False)

    def reset_wallets(self):
        self.test_forger = Wallet(name="forger", write=False)
        self.test_wallet_1 = Wallet(name="test1", write=False)
        self.test_wallet_2 = Wallet(name="test2", write=False)

    def chain_with_wallets(self):
        test_chain = Chain()
        return test_chain

    def create_too_many_transactions(self, tx_cnt):
        transaction_list = []
        for tx_idx in range(0, tx_cnt):
            transaction = self.test_wallet_1.createTransaction(
                10, self.test_wallet_2.get_public_key(), 0.1 * 10
            )
            transaction_list.append(transaction)
        return transaction_list

    def create_valid_transactions(self):
        transaction1 = self.test_wallet_1.createTransaction(
            10, self.test_wallet_2.get_public_key(), 0.1 * 10
        )
        transaction2 = self.test_wallet_2.createTransaction(
            20, self.test_wallet_1.get_public_key(), 0.1 * 20
        )
        transaction3 = self.test_wallet_1.createTransaction(
            30, self.test_wallet_2.get_public_key(), 0.1 * 30
        )
        return [transaction1, transaction2, transaction3]

    def test_genesis(self):
        test_chain = Chain()
        genesis_block = Block(
            index=0,
            previousHash=0,
            transactions=[Transaction(1, "Genesis", "Viniele", 0)],
            forger=settings.genesis_dev_address,
        )
        genesis_from_chain = test_chain._last_block
        self.assertEqual(genesis_block.toJson(), genesis_from_chain.toJson())
        del test_chain

    def test_add_valid_block(self):
        test_chain = self.chain_with_wallets()
        transactions = self.create_valid_transactions()
        block = self.test_forger.createBlock(
            test_chain.last_index() + 1, transactions, test_chain._last_block.getHash
        )
        self.assertTrue(test_chain.push_block(block))
        self.reset_wallets()
        del test_chain

    def test_add_invalid_index_block(self):
        test_chain = self.chain_with_wallets()
        transactions = self.create_valid_transactions()
        block = self.test_forger.createBlock(
            0, transactions, test_chain._last_block.getHash
        )
        with self.assertRaises(BlockValidationError):
            test_chain.push_block(block)
        self.reset_wallets()
        del test_chain

    def test_add_invalid_signature_block(self):
        test_chain = self.chain_with_wallets()
        transactions = self.create_valid_transactions()
        block = self.test_forger.createBlock(
            test_chain.last_index() + 1, transactions, test_chain._last_block.getHash
        )
        block.sign_block(self.test_wallet_1.sign("invalid signature"))
        with self.assertRaises(BlockValidationError) as err:
            test_chain.push_block(block)
        self.assertEqual(
            "Message: Invalid signature !, Arguments: {}", str(err.exception)
        )
        self.reset_wallets()
        del test_chain

    def test_add_invalid_transaction_count_block(self):
        test_chain = self.chain_with_wallets()
        transactions = self.create_too_many_transactions(settings.block_size + 1)
        block = self.test_forger.createBlock(
            test_chain.last_index() + 1, transactions, test_chain._last_block.getHash
        )
        with self.assertRaises(BlockValidationError) as err:
            test_chain.push_block(block)
        self.assertEqual(
            "Message: Transaction number exceeds the max !, Arguments: {}",
            str(err.exception),
        )
        self.reset_wallets()
        del test_chain

    def test_add_valid_transaction(self):
        test_chain = self.chain_with_wallets()
        test_transaction = self.test_wallet_1.createTransaction(
            10, self.test_wallet_2.get_public_key(), 0.1 * 10
        )
        self.assertTrue(test_chain.transaction_validation(test_transaction))
        self.reset_wallets()
        del test_chain

    def test_add_invalid_balance_transaction(self):
        test_chain = self.chain_with_wallets()
        test_transaction = self.test_wallet_1.createTransaction(
            1000, self.test_wallet_2.get_public_key(), 0.1 * 10
        )
        with self.assertRaises(TransactionValidationError) as err:
            test_chain.transaction_validation(test_transaction)
        self.assertEqual(
            "Message: Invalid balance !, Arguments: {}", str(err.exception)
        )
        self.reset_wallets()
        del test_chain

    def test_add_invalid_signature_transaction(self):
        test_chain = self.chain_with_wallets()
        test_transaction = self.test_wallet_1.createTransaction(
            10, self.test_wallet_2.get_public_key(), 0.1 * 10
        )
        test_transaction.sign_transaction(self.test_forger.sign("invalid signature"))
        with self.assertRaises(TransactionValidationError) as err:
            test_chain.transaction_validation(test_transaction)
        self.assertEqual(
            "Message: Transaction signature not valid !, Arguments: {}",
            str(err.exception),
        )
        self.reset_wallets()
        del test_chain

    def test_add_invalid_low_amount_transaction(self):
        test_chain = self.chain_with_wallets()
        test_transaction = self.test_wallet_1.createTransaction(
            -5, self.test_wallet_2.get_public_key(), 0.1 * 10
        )
        with self.assertRaises(TransactionValidationError) as err:
            test_chain.transaction_validation(test_transaction)
        self.assertEqual(
            "Message: Transaction amount too low !, Arguments: {}", str(err.exception)
        )
        self.reset_wallets()
        del test_chain

    def test_add_invalid_low_fee_transaction(self):
        test_chain = self.chain_with_wallets()
        test_transaction = self.test_wallet_1.createTransaction(
            20, self.test_wallet_2.get_public_key(), 0.01
        )
        with self.assertRaises(TransactionValidationError) as err:
            test_chain.transaction_validation(test_transaction)
        self.assertEqual(
            "Message: Fee lower than minimum !, Arguments: {}", str(err.exception)
        )
        self.reset_wallets()
        del test_chain

    def test_add_invalid_same_accounts_transaction(self):
        test_chain = self.chain_with_wallets()
        test_transaction = self.test_wallet_1.createTransaction(
            20, self.test_wallet_1.get_public_key(), 0.1 * 20
        )
        with self.assertRaises(TransactionValidationError) as err:
            test_chain.transaction_validation(test_transaction)
        self.assertEqual(
            "Message: Transaction payer is the same as payee !, Arguments: {}",
            str(err.exception),
        )
        self.reset_wallets()
        del test_chain

    def test_insert_account(self):
        test_chain = Chain()
        test_chain.insert_account(self.test_forger.get_public_key())
        result = test_chain.check_account_at_address(self.test_forger.get_public_key())
        self.assertTrue(result)
        self.reset_wallets()
        del test_chain

    def test_remove_transactions(self):
        test_chain = Chain()
        transactions = self.create_valid_transactions()
        transactions_to_remove = transactions[0:2]
        transactions_to_check = [transactions[-1]]
        for trans in transactions:
            test_chain.pendingTransactions.append(trans)
        test_chain.remove_transactions(transactions_to_remove)
        out_transactions = test_chain.pendingTransactions
        for t_idx in range(0, len(out_transactions)):
            self.assertEqual(
                out_transactions[t_idx].toJson(), transactions_to_check[t_idx].toJson()
            )
        self.reset_wallets()
        del test_chain

    def test_process_block(self):
        test_chain = self.chain_with_wallets()
        transactions = self.create_valid_transactions()
        block = self.test_forger.createBlock(
            test_chain.last_index() + 1, transactions, test_chain._last_block.getHash
        )
        test_chain.process_block(block)
        test_transaction = Transaction(
            6,
            settings.genesis_dev_address,
            block.get_forger(),
            fee=settings.minimum_fee,
            type="REWARD",
        )
        self.assertEqual(
            test_transaction.toJson(), test_chain.pendingTransactions[-1].toJson()
        )
        self.reset_wallets()
        del test_chain

    def test_execute_transactions(self):
        test_chain = self.chain_with_wallets()
        transactions = self.create_valid_transactions()
        test_chain.execute_transactions(transactions)
        balance_acc1 = test_chain.account_model.get_balance(
            self.test_wallet_1.get_public_key()
        )
        balance_acc2 = test_chain.account_model.get_balance(
            self.test_wallet_2.get_public_key()
        )
        self.assertEqual(balance_acc1, 76)
        self.assertEqual(balance_acc2, 118)
        self.reset_wallets()
        del test_chain

    def test_invalid_balance_account_model(self):
        test_chain = Chain()
        with self.assertRaises(AccountModelError) as err:
            test_chain.account_model.get_balance(self.test_wallet_1.get_public_key())
        self.assertEqual(
            "Message: Account not found -get !, Arguments: {}", str(err.exception)
        )
        del test_chain

    def test_invalid_update_account_model(self):
        test_chain = Chain()
        with self.assertRaises(AccountModelError) as err:
            test_chain.account_model.balance_update(
                self.test_wallet_1.get_public_key(), 420
            )
        self.assertEqual(
            "Message: Account not found -update !, Arguments: {}", str(err.exception)
        )
        del test_chain


if __name__ == "__main__":
    unittest.main()
