from typing import List

import requests

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
        self._blockSize = 10
        self._nodes = set()
        self._wallets = List[Wallet]
        # Defining the first block in the chain
        self.genesis()

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
        self.new_block(0, 0, Transaction(1, "Genesis", "Viniele", 0))

    # return data about a certain wallet, iterating through the chain
    def get_wallet_data(self, wallet_address):
        if wallet_address in self.get_wallet_addresses():
            pass

    def new_block(self, proof, previousHash, transaction):
        block = Block(len(self.chain), proof, previousHash, transaction)
        self.next_block_chooser.scan_block(block)

    # check that the signature corresponds to transaction
    # signed by the public key (sender_address)
    def addBlock(self, senderKey, signature, transaction):
        publicKey = RSA.importKey(binascii.unhexlify(senderKey))
        verifier = PKCS1_v1_5.new(publicKey)
        _hash = SHA.new(transaction.toString().encode('utf8'))

        if verifier.verify(_hash, binascii.unhexlify(signature)):
            self.pendingTransactions.append(transaction)

    # used in order to update the chain state when new block data occurs
    def process_block(self, block):
        pass

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

    def unsigned_transaction(self, payer_address):
        pass

    def block_validator(self, block):


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

    
