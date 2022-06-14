import errno
from glob import glob
from urllib import response
from flask_classful import FlaskView, route
from flask import Flask, jsonify, request

from Exceptions import APIError
import Utils as Utls


class NodeAPI(FlaskView):

    node = None

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, ip: str, api_port: int):
        NodeAPI.register(self.app, route_base="/")
        self.app.run(host=ip, port=api_port)

    def inject_node(self, nodeToInj):
        global node
        node = nodeToInj

    @route("/info", methods=["GET"])
    def info_method(self):
        return "Communication interface of Node class", 200

    @route("/blockchain", methods=["GET"])
    def blockchain_method(self):
        return node.blockchain.toJson(), 200

    @route("/pool", methods=["GET"])
    def transactionPool_method(self):
        transaction_dict = {}
        for cnt, transaction in enumerate(node.blockchain.pendingTransactions):
            transaction_dict[cnt] = transaction.toJson()

        return jsonify(transaction_dict), 200

    @route("/transaction", methods=["POST"])
    def transaction_method(self):
        values = request.get_json()
        if "transaction" not in values:
            err_text = (
                "POST transaction method failed due to wrong object request value !"
            )
            return err_text, 400

        # get and handle the transactions
        transaction = Utls.decode(values["transaction"])
        node.handle_transaction(transaction)
        response = {"message": "Received transaction"}
        return jsonify(response), 201
