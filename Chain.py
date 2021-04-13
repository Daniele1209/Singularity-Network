from Block import Block
from Transaction import Transaction
from Crypto.Hash import SHA, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii

class Chain:

    def __init__(self):
        self._chain = []
        self._nodes = set()
        # Defining the first block in the chain
        self.Genesis()
    
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
        hash = SHA.new(transaction.toString().encode('utf8'))
        isValid = verifier.verify(hash, binascii.unhexlify(signature))

        if isValid:
            lastBlock = self.lastBlock()
            lastProof = lastBlock.proof
            proof_no = self.mine(lastProof)

            blockToAdd = Block(len(self._chain), proof_no ,self.lastBlock().getHash(), transaction)
            self.mine(blockToAdd._nonce)
            self._chain.append(blockToAdd)

    @property
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
            hash.update(str(nonce + solution))

            attempt = hash.hexdigest()

            if attempt[0:4] == "0000":
                print("Solved !")
                print(solution)
                return solution
            
            solution += 1


    
