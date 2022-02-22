from BlockChain.Wallet.Wallet import Wallet
from Chain import Chain
from P2P.p2p_network import *

class UI:

    def __init__(self):
        #self._User = input("Enter a username >>> ")
        self._Wallet = None
        self._Chain = Chain()

    def run(self):
        print(r"""
                        ███████╗██╗███╗   ██╗ ██████╗ ██╗   ██╗██╗      █████╗ ██████╗ ██╗████████╗██╗   ██╗ ██████╗ ██████╗ ██╗███╗   ██╗
                        ██╔════╝██║████╗  ██║██╔════╝ ██║   ██║██║     ██╔══██╗██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝██╔════╝██╔═══██╗██║████╗  ██║
                        ███████╗██║██╔██╗ ██║██║  ███╗██║   ██║██║     ███████║██████╔╝██║   ██║    ╚████╔╝ ██║     ██║   ██║██║██╔██╗ ██║
                        ╚════██║██║██║╚██╗██║██║   ██║██║   ██║██║     ██╔══██║██╔══██╗██║   ██║     ╚██╔╝  ██║     ██║   ██║██║██║╚██╗██║
                        ███████║██║██║ ╚████║╚██████╔╝╚██████╔╝███████╗██║  ██║██║  ██║██║   ██║      ██║   ╚██████╗╚██████╔╝██║██║ ╚████║
                        ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝
        """)

        self._Wallet = Wallet(self._Chain)

       
        satoshi = Wallet(self._Chain)
        alice = Wallet(self._Chain)

        print(":moneybag: wallets created ! :moneybag:")

        self._Wallet.sendCoins(10, satoshi._publicKey)
        satoshi.sendCoins(10, self._Wallet._publicKey)
        alice.sendCoins(10, self._Wallet._publicKey)
        print(":credit_card: Transactions are pending ! :credit_card:")
        print(self._Chain._pendingTransactions)

        # Processing pending transactions
        print(":pick: Mining pending transactions ! :pick:")
        self._Chain.minePending(satoshi._publicKey)
        print(self._Chain._pendingTransactions)

        self._Chain.print_chain()

        #self._Chain.register_node()

        #print(self._Wallet.get_coins())
        

ui = UI()
ui.run()