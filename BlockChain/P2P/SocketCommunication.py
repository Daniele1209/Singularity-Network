from p2pnetwork.node import Node

class SocketCommunication(Node):

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)

    # Open the port
    def startSocketCommunication(self):
        self.start()

    def inbound_node_connected(self, node):
        print('Inbound connection')

    def outbound_node_connected(self, node):
        print('Outbound connection')
