import sys

from Wallet.Wallet import Wallet
from Chain import Chain
from Node import Node
from pyfiglet import Figlet, figlet_format
import requests
import json

import Utils as Utls


class UI:
    def __init__(self):
        pass

    def run(self):
        print()
        print(figlet_format("Inari Network", font="slant"))

        # argv[0] - name of program
        # argv[1] - ip
        # argv[0] - port
        ip = sys.argv[1]
        port = int(sys.argv[2])
        api_port = int(sys.argv[3])

        node = Node(ip, port)
        node.startP2P()
        node.startAPI(api_port)

        # used for testing on multiple ports
        if port == 10002:
            node.p2p.connect_with_node("localhost", 10001)

            # json_object = json.dumps(package, indent = 4)
            # # Writing to sample.json
            # with open("test_req.json", "w") as outfile:
            #     outfile.write(json_object)
            # request = requests.posst(url, json=package)
            # print(request.text)

        print(node.blockchain.toJson())
        # print(node.wallet.toJson())

        print("💰 wallets created ! 💰")

        print("💳 Transactions are pending ! 💳")

        # Processing pending transactions
        print("⛏️ Node working ... ⛏️")


ui = UI()
ui.run()
