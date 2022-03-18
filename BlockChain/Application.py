from BlockChain.Wallet.Wallet import Wallet
from Chain import Chain
from Node import Node

import emoji


class UI:

    def __init__(self):
        pass

    def run(self):
        print(r"""
                        ███████╗██╗███╗   ██╗ ██████╗ ██╗   ██╗██╗      █████╗ ██████╗ ██╗████████╗██╗   ██╗ ██████╗ ██████╗ ██╗███╗   ██╗
                        ██╔════╝██║████╗  ██║██╔════╝ ██║   ██║██║     ██╔══██╗██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝██╔════╝██╔═══██╗██║████╗  ██║
                        ███████╗██║██╔██╗ ██║██║  ███╗██║   ██║██║     ███████║██████╔╝██║   ██║    ╚████╔╝ ██║     ██║   ██║██║██╔██╗ ██║
                        ╚════██║██║██║╚██╗██║██║   ██║██║   ██║██║     ██╔══██║██╔══██╗██║   ██║     ╚██╔╝  ██║     ██║   ██║██║██║╚██╗██║
                        ███████║██║██║ ╚████║╚██████╔╝╚██████╔╝███████╗██║  ██║██║  ██║██║   ██║      ██║   ╚██████╗╚██████╔╝██║██║ ╚████║
                        ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝
        """)

        node = Node()

        print(node.blockchain.toJson())
        print(node.wallet.toJson())

        print("💰 wallets created ! 💰")

        print(emoji.emojize(":credit_card: Transactions are pending ! :credit_card:"))

        # Processing pending transactions
        print(emoji.emojize(":pick: Mining pending transactions ! :pick:"))


ui = UI()
ui.run()