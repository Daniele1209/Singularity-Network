import BlockChain.Utils
from BlockChain.Block import Block
from BlockChain.Chain import Chain
from BlockChain.P2P.Message import Message
from BlockChain.P2P.SocketCommunication import SocketCommunication
from BlockChain.Wallet.Wallet import Wallet

import copy


class Node:
    def __init__(self, ip, port, keyfile):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.keyfile = keyfile

        self.blockchain = Chain()
        # Initializer for the test wallet
        self.wallet = Wallet()

        if keyfile is not None:
            self.wallet.generateFromPair(keyfile[0], keyfile[1])

    def get_wallet(self):
        return self.wallet

    def get_blockchain(self):
        return self.blockchain

    def handle_transaction(self, transaction):
        if self.blockchain.check_block_transaction(transaction):
            self.blockchain.insert_transaction(transaction)
            message = Message(self.p2p.socketConnector, "TRANSACTION", transaction)
            # Encode the message
            message_encoded = BlockChain.Utils.encode(message)
            # Broadcast the encoded message
            self.p2p.broadcast(message_encoded)
            # Check if a new forger is required
            if self.blockchain.forger_required():
                self.forge_block()

    def handle_block(self, block: Block):
        # signature_valid = Wallet.check_verified(
        #     block.payload(), block.get_signature(), block.get_forger()
        # )

        # check of a a blockchain is in sync with the network
        # if not, update the blocks
        if not self.blockchain.check_block_count(block):
            print("REQUEST CHAIN\n")
            self.request_chain()

        if self.blockchain.check_block_identity(block):
            self.blockchain.push_block(block)

        # message = Message(self.p2p.socketConnector, "BLOCK", block)
        # # Encode the message
        # message_encoded = BlockChain.Utils.encode(message)
        # # Broadcast the encoded message
        # self.p2p.broadcast(message_encoded)

    # notifies the blockchain that is time to forge a new block
    def forge_block(self):
        chosen_forger = self.blockchain.choose_forger()
        # check if our node is the forger
        if chosen_forger == self.wallet.get_public_key():
            print("I am the chosen forger")
            new_block = self.blockchain.create_block(self.wallet)
            if new_block != None:
                message = Message(self.p2p.socketConnector, "BLOCK", new_block)
                encoded_message = BlockChain.Utils.encode(message)
                self.p2p.broadcast(encoded_message)

    # request the blockchain from other nodes
    def request_chain(self):
        message = Message(self.p2p.socketConnector, "BLOCKCHAINREQUEST", None)
        encoded_message = BlockChain.Utils.encode(message)
        self.p2p.broadcast(encoded_message)

    # send blockchain data to a certain node
    def handle_chain_request(self, request_node):
        message = Message(self.p2p.socketConnector, "BLOCKCHAIN", self.blockchain)
        encoded_message = BlockChain.Utils.encode(message)
        self.p2p.send(request_node, encoded_message)

    # update current blockchain from fetched one
    def handle_received_blockchain(self, blockchain):
        self.blockchain.sync_chain(blockchain)
        # localBlockchainCopy = copy.deepcopy(self.blockchain)
        # localBlockCount = len(localBlockchainCopy.chain)
        # receivedChainBlockCount = len(blockchain.chain)
        # if localBlockCount < receivedChainBlockCount:
        #     for blockNumber, block in enumerate(blockchain.chain):
        #         if blockNumber >= localBlockCount:
        #             localBlockchainCopy.push_block(block)
        #     self.blockchain = localBlockchainCopy

    def startP2P(self, ip: str = "localhost", port: int = 10001):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self, ip, port)
