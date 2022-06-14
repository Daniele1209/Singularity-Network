import sys

from pyfiglet import figlet_format

from BlockChain.Node import Node


class UI:
    def __init__(self):
        pass

    def run(self):
        print()
        print(figlet_format("Singularity Network", font="slant"))

        keyfile = None
        ip = sys.argv[1]
        port = int(sys.argv[2])
        api_port = int(sys.argv[3])
        origin_ip = sys.argv[4]
        origin_port = int(sys.argv[5])
        if len(sys.argv) > 7:
            keyfile = sys.argv[6], sys.argv[7]

        node = Node(ip, port, keyfile)
        node.startP2P(origin_ip, origin_port)
        node.startAPI(ip, api_port)


ui = UI()
ui.run()
