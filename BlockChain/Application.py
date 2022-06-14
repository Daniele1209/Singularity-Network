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
        node.startAPI(ip, api_port)

        # used for testing on multiple ports
        # if port == 10002:
        #     node.p2p.connect_with_node("localhost", 10001)

        # json_object = json.dumps(package, indent = 4)
        # # Writing to sample.json
        # with open("test_req.json", "w") as outfile:
        #     outfile.write(json_object)
        # request = requests.posst(url, json=package)
        # print(request.text)

        # print(node.blockchain.toJson())
        # # print(node.wallet.toJson())

        # print("💰 wallets created ! 💰")

        # print("💳 Transactions are pending ! 💳")

        # # Processing pending transactions
        # print("⛏️ Node working ... ⛏️")


ui = UI()
ui.run()
