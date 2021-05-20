from urllib.parse import urlparse
import requests

class Nodes:
    def __init__(self):
        self._nodes = set()

    # Registering an address as a node
    def registerNode(self, address):
        parsed_url = urlparse(address)
        self._nodes.add(parsed_url.netloc)

    def resolveConflicts(self):
        neighbors = self._nodes
        newChain = None;

        maxLength = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > maxLength and self.isValidChain():
                    maxLength = length
                    newChain = chain

        if newChain:
            self.chain = self.chainJSONdecode(newChain)
            print(self.chain)
            return True

        return False


