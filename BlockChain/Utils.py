from Crypto.Hash import SHA256
import json
import jsonpickle

@staticmethod
def hash(data):
    data_string = json.dumps(data)
    binary_data = data_string.encode('utf-8')
    hash_data = SHA256.new(binary_data)
    return hash_data

@staticmethod
def encode(object):
    return jsonpickle.encode(object, unpickle=True)

@staticmethod
def decode(object):
    return jsonpickle.decode(object)