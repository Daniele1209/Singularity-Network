from Crypto.Hash import SHA256
import json


def hash(data):
    data_string = json.dumps(data)
    binary_data = data_string.encode('utf-8')
    hash_data = SHA256.new(binary_data)
    return hash_data
