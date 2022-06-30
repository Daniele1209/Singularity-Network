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
        print(figlet_format("Singularity Network", font="slant"))

        keyfile = None
        # argv[0] - name of program
        # argv[1] - ip
        # argv[0] - port
        ip = sys.argv[1]
        port = int(sys.argv[2])
        api_port = int(sys.argv[3])
        origin_ip = sys.argv[4]
        origin_port = int(sys.argv[5])
        if len(sys.argv) > 7:
            keyfile = sys.argv[6], sys.argv[7]

        node = Node(ip, port, keyfile)
        node.startP2P(origin_ip, origin_port)
        node.startAPI(api_port)


ui = UI()
ui.run()
