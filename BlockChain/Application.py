import sys

from BlockChain.Wallet.Wallet import Wallet
from Chain import Chain
from Node import Node
from pyfiglet import Figlet, figlet_format
from termcolor import colored

import emoji


class UI:

    def __init__(self):
        pass

    def run(self):
        print((colored(figlet_format("SingularityCoin", font='slant'), color="blue")))

        # argv[0] - name of program
        # argv[1] - ip
        # argv[0] - port
        ip = sys.argv[1]
        port = int(sys.argv[2])

        node = Node(ip, port)
        node.startP2P()

        print(node.blockchain.toJson())
        print(node.wallet.toJson())

        print("💰 wallets created ! 💰")

        print(emoji.emojize(":credit_card: Transactions are pending ! :credit_card:"))

        # Processing pending transactions
        print(emoji.emojize(":pick: Node working ... :pick:"))


ui = UI()
ui.run()