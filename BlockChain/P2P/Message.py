from BlockChain.AdditionalTypes import MESSAGE_TYPE


class Message:
    message_type: MESSAGE_TYPE

    def __init__(self, sender_connector, message_type: MESSAGE_TYPE, data):
        self.sender_connector = sender_connector
        self.message_type = message_type
        self.data = data
