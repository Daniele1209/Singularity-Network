import sys

from Wallet.Wallet import Wallet
from Chain import Chain
from Node import Node
from pyfiglet import Figlet, figlet_format


class UI:

    def __init__(self):
        pass

    def run(self):
        print()
        print(figlet_format("SingularityCoin", font='slant'))

        # argv[0] - name of program
        # argv[1] - ip
        # argv[0] - port
        ip = sys.argv[1]
        port = int(sys.argv[2])

        node = Node(ip, port)
        node.startP2P()

        # used for testing on multiple ports
        if port == 10002:
            node.p2p.connect_with_node('localhost', 10001)

        print(node.blockchain.toJson())
        #print(node.wallet.toJson())

        print("💰 wallets created ! 💰")

        print("💳 Transactions are pending ! 💳")

        # Processing pending transactions
        print("⛏️ Node working ... ⛏️")


ui = UI()
ui.run()