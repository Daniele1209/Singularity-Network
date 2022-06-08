from typing import List

import requests


from Exceptions import (
    TransactionValidationError,
    BlockValidationError,
    BlockProcessingError,
    AccountModelError,
)
from Config import genesis_dev_address, block_size, minimum_fee

from Message import Message

from Block import *
from Transaction import Transaction
from Block_chooser import BlockChooser
from Wallet.Wallet import Wallet
from Account_model import AccountModel
from Consensus.Proof_of_stake import ProofOfStake
import Utils

from Crypto.Hash import SHA, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from urllib.parse import urlparse
import binascii
import logging


class Chain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pendingTransactions: List[Transaction] = []
        self._blockSize = block_size
        self._minimum_fee = minimum_fee
        # Defining the first block in the chain
        self.genesis_hash = self.genesis()

        self.account_model = AccountModel()
        # self.next_block_chooser = BlockChooser(self)
        # self.next_block_chooser.start()
        self.pos = ProofOfStake()

    # when we download and sync all the blockchain history
    def sync_chain(self, current_chain):
        self.chain = current_chain.chain
        self.pendingTransactions = current_chain.pendingTransactions

    def genesis(self):
        block_to_add = Block(
            index=0,
            previousHash=0,
            transactions=[Transaction(1, "Genesis", "Viniele", 0)],
            forger=genesis_dev_address,
        )
        self.chain.append(block_to_add)
        return block_to_add.getHash

    def insert_account(self, account):
        self.account_model.add_account(account)

    # return data about a certain wallet, iterating through the chain
    def get_wallet_data(self, wallet_address):
        if wallet_address in self.account_model.get_accounts():
            return self.account_model.get_balance(wallet_address)

    def get_last_hash(self):
        return Utils.hash(self._last_block.payload()).hexdigest()

    # def new_block(self, block):
    #     self.next_block_chooser.scan_block(block)

    """
    # check that the signature corresponds to transaction
    # signed by the public key (sender_address)
    def addBlock(self, senderKey, signature, transaction):
        publicKey = RSA.importKey(binascii.unhexlify(senderKey))
        verifier = PKCS1_v1_5.new(publicKey)
        _hash = SHA.new(transaction.toString().encode('utf8'))

        if verifier.verify(_hash, binascii.unhexlify(signature)):
            self.pendingTransactions.append(transaction)
    """

    def insert_transaction(self, transaction):
        # check transaction signature
        signature_valid = self.transaction_validation(transaction)
        # check if transaction already exists
        transaction_exists = self.check_transaction(transaction)

        if signature_valid and transaction_exists:
            self.pendingTransactions.append(transaction)
        else:
            raise TransactionValidationError(
                "Transaction signature not valid or already existing !"
            )

    def remove_transactions(self, transactions):
        for transaction in transactions:
            for pool_transaction in self.pendingTransactions:
                if transaction.equals(pool_transaction):
                    self.pendingTransactions.remove(pool_transaction)

    def push_block(self, block):
        if self.block_validation(block):
            self.execute_transactions(block.get_transactions())
            self.chain.append(block)
            self.remove_transactions(block.get_transactions())
            return True
        return False

    # used in order to update the chain state when new block data occurs
    def process_block(self, block):
        fees = 0.0
        if self.block_validation(block):
            for transaction in block.get_transactions():
                fees += transaction.get_fee()
            self.push_block(block)
            self.remove_transactions(block.get_transactions())
            reward_transaction = self.unsigned_transaction(
                fees,
                genesis_dev_address,
                block.get_forger(),
                fee=minimum_fee,
                type="REWARD",
            )
            self.pendingTransactions.append(reward_transaction)
        return True

    # iterate through the blockchain, get each block and find the
    # user transactions so that you can determine his balance
    def getWalletBalance(self, wallet):
        total = 0
        for block_idx in range(0, len(self.chain)):
            for current_trans in self.chain[block_idx].get_transactions():
                if current_trans.get_payer() == wallet:
                    total -= current_trans.get_amount()
                if current_trans.get_payee() == wallet:
                    total += current_trans.get_amount()

        return total

    """
    We have 2 cases of transaction, the transfer one and the stake
    In the stake transaction the amount of coins that a user has is locked
    """

    def execute_transaction(self, transaction):
        if transaction.type == "STAKE":
            sender = transaction.get_payer()
            receiver = transaction.get_payee()
            if sender == receiver:
                stake_amount = transaction.get_amount()
                self.pos.update(sender, stake_amount)
                # update account balance, locking the staked amount
                self.account_model.balance_update(sender, -amount)
        else:
            sender_account = transaction.get_payer()
            receiver_account = transaction.get_payee()
            amount = transaction.get_amount()
            fee = transaction.get_fee()
            self.account_model.balance_update(sender_account, -(amount + fee))
            self.account_model.balance_update(receiver_account, amount)

    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    # checks if a certain transaction already exists
    def check_transaction(self, transaction):
        for trans in self.pendingTransactions:
            if transaction.equals(trans):
                return False
        return True

    # creates unsigned transaction object
    def unsigned_transaction(self, amount, payer_address, payee_address, fee, type):
        built_transaction = Transaction(
            amount=amount, payer=payer_address, payee=payee_address, fee=fee, type=type
        )
        return built_transaction

    # check if a certain amount of transactions have been reached in the pool
    # this signals if the time for a new forger has come
    def forger_required(self):
        if len(self.pendingTransactions) >= self._blockSize:
            return True
        return False

    def choose_forger(self):
        last_block_hash = self.get_last_hash()
        next_forger = self.pos.selectForger(last_block_hash)
        return next_forger

    # used in order to check the integrity of the wanted block
    # checking: index, signature, transaction count
    def block_validation(self, block):
        # check if the block to be verified is the genesis one
        if block.get_index() == 0:
            if block.getHash == self.genesis_hash:
                raise BlockValidationError("Block hash invalid ! Same as genesis")
        if block.get_index() != self._last_block.get_index() + 1:
            raise BlockValidationError("Block index does not belong to the sequence")
        if not block.check_verified(
            block.payload(), block.get_signature(), block.get_forger()
        ):
            raise BlockValidationError("Invalid signature !")
        if len(block.get_transactions()) > block_size:
            raise BlockValidationError("Transaction number exceeds the max !")
        # check if all transactions in block are valid
        for transaction in block.get_transactions():
            if not self.transaction_validation(transaction):
                raise BlockValidationError(
                    f"Transaction in block not valid: {transaction.toJson()}"
                )

        return True

    # used in order to check if the transaction parameters are in order
    # checking: signature, amount, fee, payer/payee
    def transaction_validation(self, transaction):
        sender_balance = self.account_model.get_balance(transaction.get_payer())
        print(
            "PAYER BALANCE :::: "
            + str(sender_balance)
            + " :::: "
            + transaction.get_type()
        )
        print(self.account_model.get_accounts())
        if transaction.get_type() == "EXCHANGE":
            return True
        if int(sender_balance) < int(transaction.get_amount()):
            print("Invalid balance !")
            raise TransactionValidationError("Invalid balance !")
        if not transaction.check_verified(
            transaction.payload(), transaction.get_signature(), transaction.get_payer()
        ):
            raise TransactionValidationError("Transaction signature not valid !")
        if transaction.get_amount() < 0:
            raise TransactionValidationError("Transaction amount too low !")
        if transaction.get_fee() < self._minimum_fee:
            raise TransactionValidationError("Fee lower than minimum !")
        if transaction.get_payer() == transaction.get_payee():
            raise TransactionValidationError("Transaction payer is the same as payee !")

        return True

    def last_index(self):
        return self._last_block.get_index()

    def check_account_at_address(self, address):
        if address in self.account_model.get_accounts():
            return True
        return False

    # return latest block
    @property
    def _last_block(self):
        return self.chain[-1]

    def toJson(self):
        data = {}
        data["chain"] = []
        for block in self.chain:
            data["chain"].append(block.toJson())
        return data
