import sys

from config import settings

from pyfiglet import figlet_format

from BlockChain.Node import Node
from BlockChain.NodeAPI import NodeAPI


class UI:
    def __init__(self):
        pass

    def run(self):
        print()
        print(figlet_format("Singularity Network", font="slant"))

        keyfile = None

        ip = sys.argv[1] if len(sys.argv) > 1 else settings.host_ip
        port = int(sys.argv[2]) if len(sys.argv) > 2 else settings.host_port
        api_port = int(sys.argv[3]) if len(sys.argv) > 3 else settings.host_api_port
        origin_ip = sys.argv[4] if len(sys.argv) > 4 else settings.origin_ip
        origin_port = int(sys.argv[5]) if len(sys.argv) > 5 else settings.origin_port
        
        if len(sys.argv) > 7:
            keyfile = sys.argv[6], sys.argv[7]

        node = Node(ip, port, keyfile)
        node.startP2P(origin_ip, origin_port)

        api = NodeAPI(node)
        api.start(ip, api_port)


ui = UI()
ui.run()
