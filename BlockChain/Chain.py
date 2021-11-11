import requests

from BlockChain.Block import *
from Transaction import Transaction
from Crypto.Hash import SHA, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from urllib.parse import urlparse
import binascii

class Chain:

    def __init__(self):
        self._chain = []
        self._pendingTransactions = []
        self._blockSize = 10
        self._nodes = set()
        # Defining the first block in the chain
        self.Genesis()
        #User reward for mining
        self._reward = 20
    
    def Genesis(self):
        self.newBlock(0, 0, Transaction(1, "Genesis", "Viniele"))

    def newBlock(self, proof, previousHash, transaction):
        block = Block(len(self._chain), proof, previousHash, transaction)
        self._chain.append(block)

        return block

    # check that the signature corresponds to transaction
    # signed by the public key (sender_address)
    def addBlock(self, senderKey, signature, transaction):
        publicKey = RSA.importKey(binascii.unhexlify(senderKey))
        verifier = PKCS1_v1_5.new(publicKey)
        _hash = SHA.new(transaction.toString().encode('utf8'))

        if verifier.verify(_hash, binascii.unhexlify(signature)):
            self._pendingTransactions.append(transaction)

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

    # itereate through the blockchain and find the user transactions so that you can determine
    # his balance
    def getWalletBalance(self, wallet):
        total = 0
        for block in self._chain:
            if block._transaction._payer == wallet:
                total -= block._transaction._amount
            if block._transaction._payee == wallet:
                total += block._transaction._amount
            
        return total

        
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


    
