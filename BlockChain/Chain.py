from typing import List

import requests

from Exceptions import *
from Config import genesis_dev_address, block_size, minimum_fee

from BlockChain.Block import *
from BlockChain.Transaction import Transaction
from Block_chooser import BlockChooser
from Wallet.Wallet import Wallet

from Crypto.Hash import SHA, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from urllib.parse import urlparse
import binascii

class Chain:

    def __init__(self):
        self.chain: List[Block] = []
        self.pendingTransactions: List[Transaction] = []
        self._blockSize = block_size
        self._nodes = set()
        self._minimum_fee = minimum_fee
        self._wallets = List[Wallet]
        # Defining the first block in the chain
        self.genesis_hash = self.genesis()

        self.next_block_chooser = BlockChooser(self)
        self.next_block_chooser.start()

    def get_wallet_addresses(self):
        address_list = []
        for wallet_idx in range(len(self._wallets)):
            address_list.append(self._wallets[wallet_idx])
        return address_list

    # when we download and sync all the blockchain history
    def sync_chain(self, current_chain):
        self.chain = current_chain.chain
        self.pendingTransactions = current_chain.pendingTransactions

    def genesis(self):
        block_to_add = Block(index=0, previousHash=0, transactions=[Transaction(1, "Genesis", "Viniele", 0)],
                             forger=genesis_dev_address)
        self.new_block(block_to_add)
        return block_to_add.getHash

    def insert_wallet(self, wallet):
        self._wallets.append(wallet)

    # return data about a certain wallet, iterating through the chain
    def get_wallet_data(self, wallet_address):
        wallet_list = self.get_wallet_addresses()
        if wallet_address in wallet_list:
            for wallet_idx in range(0, len(wallet_list)):
                if wallet_list[wallet_idx].get_public_key() == wallet_address:
                    return wallet_list[wallet_idx].toJson

    def new_block(self, block):
        self.next_block_chooser.scan_block(block)

    # used each time a block is added to the chain
    # refresh the state of the chain
    def insert_block_in_chain(self, block):
        pass

    # check that the signature corresponds to transaction
    # signed by the public key (sender_address)
    def addBlock(self, senderKey, signature, transaction):
        publicKey = RSA.importKey(binascii.unhexlify(senderKey))
        verifier = PKCS1_v1_5.new(publicKey)
        _hash = SHA.new(transaction.toString().encode('utf8'))

        if verifier.verify(_hash, binascii.unhexlify(signature)):
            self.pendingTransactions.append(transaction)

    def push_block(self, block):
        self.chain.append(block)
        self.pendingTransactions.clear()

    # used in order to update the chain state when new block data occurs
    def process_block(self, block):
        fees = 0.0
        if self.block_validation(block):
            for transaction in block.get_transactions:
                fees += transaction.get_fee()
            self.push_block(block)
            reward_transaction = self.unsigned_transaction(fees, genesis_dev_address,
                                                           block.get_forger(), fee=minimum_fee, type='REWARD')
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

    # creates unsigned transaction object
    def unsigned_transaction(self, amount, payer_address, payee_address, fee, type):
        built_transaction = Transaction(
            amount=amount,
            payer=payer_address,
            payee=payee_address,
            fee=fee,
            type=type
        )
        return built_transaction

    # used in order to check the integrity of the wanted block
    # checking: index, signature, transaction count
    def block_validation(self, block):
        # check if the block to be verified is the genesis one
        if block.get_index() == 0:
            if block.getHash == self.genesis_hash:
                raise BlockValidationError('Block hash invalid ! Same as genesis')
        if block.get_index() != self._last_block.get_index() + 1:
            raise BlockValidationError('Block index does not belong to the sequence')
        if not block.check_verified:
            raise BlockValidationError('Invalid signature !')
        if len(block.get_transactions()) > block_size:
            raise BlockValidationError('Transaction number exceeds the max !')

        return True

    # used in order to check if the transaction parameters are in order
    # checking: signature, amount, fee, payer/payee
    def transaction_validation(self, transaction):
        if not transaction.signed():
            raise TransactionValidationError('Transaction signature not valid !')
        if transaction.get_amount() < 0:
            raise TransactionValidationError('Transaction amount too low !')
        if transaction.get_fee() < self._minimum_fee:
            raise TransactionValidationError('Fee lower than minimum !')
        if transaction.get_payee() == transaction.get_payee():
            raise TransactionValidationError('Transaction payer is the same as payee !')

        return True


    # return latest block
    @property
    def _last_block(self):
        return self.chain[-1]

    """
    # get transactions from list of pending transactions and process them
    def minePending(self, miner):
        if len(self._pendingTransactions) <= 0:
            print("Nothing to mine ! :(")
            return False

        else:
            transaction = self._pendingTransactions.pop(0)
        
            lastBlock = self.lastBlock()
            lastProof = lastBlock.get_proof()
            proof_no = self.mine(lastProof)
            blockToAdd = Block(len(self._chain), proof_no, lastBlock.getHash, transaction)
            #self.mine(blockToAdd.get_nonce())

            self._chain.append(blockToAdd)

            minerReward = Transaction(self._reward, "system", miner)
            self._pendingTransactions.append(minerReward)

        return True

    def registerNode(self, address):
        parsed_url = urlparse(address)
        self._nodes.add(parsed_url.netloc)

    def resolveConflicts(self):
        neighbors = self._nodes
        newChain = None;

        maxLength = len(self.chain)
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > maxLength and self.isValidChain():
                    maxLength = length
                    newChain = chain

        if newChain:
            self.chain = self.chainJSONdecode(newChain)
            print(self.chain)
            return True

        return False

    def lastBlock(self):
        return self._chain[-1]

    @staticmethod
    def checkValidity(block, prevBlock):
        if prevBlock.index + 1 != block.index:
            return False

        if prevBlock.getHash != block.previousHash:
            return False
        
    def mine(self, nonce):
        solution = 1
        print("Mining ...")

        # Create hash using the MD5 algorithm untill we find one that starts with "0000"
        # Then it can be sent to other nodes to be verified
        while True:
            hash = MD5.new()
            hash.update(str(nonce + solution).encode('utf8'))

            attempt = hash.hexdigest()

            if attempt[0:4] == "1234":
                print("Solved !")
                print(solution)
                return solution
            
            solution += 1

    def print_chain(self):
        for block in self._chain:
            print(block)
    """

    
