class SocketConnector:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def equals(self, connector):
        if connector.ip == self.ip and connector.port == self.port:
            return True
        return False
