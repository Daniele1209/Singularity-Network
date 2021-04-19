from Wallet import Wallet
from Chain import Chain

class UI:

    def __init__(self):
        self._User = input("Enter a username >>> ")
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

        print("wallets created !")

        self._Wallet.sendCoins(10, satoshi._publicKey)
        satoshi.sendCoins(10, self._Wallet._publicKey)
        alice.sendCoins(10, self._Wallet._publicKey)

        print(self._Chain)


ui = UI()
ui.run()