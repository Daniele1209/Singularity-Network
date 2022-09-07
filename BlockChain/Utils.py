import json

import jsonpickle
from Crypto.Hash import SHA256


def hash(data):
    data_string = json.dumps(data)
    binary_data = data_string.encode("utf-8")
    hash_data = SHA256.new(binary_data)
    return hash_data


def encode(object):
    return jsonpickle.encode(object, unpicklable=True)


def decode(object):
    return jsonpickle.decode(object)
