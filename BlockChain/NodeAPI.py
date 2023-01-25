from __future__ import annotations
from crypt import methods
import errno
from glob import glob
from urllib import response
from flask_classful import FlaskView, route
from flask import Flask, jsonify, request

from typing import TYPE_CHECKING

from flask import Flask, jsonify, request
from flask_classful import FlaskView, route

import BlockChain.Utils as Utls

if TYPE_CHECKING:
    from BlockChain.Node import Node


class NodeAPI(FlaskView):
    node = None

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, ip: str, api_port: int, node_input: Node):
        global node
        node = node_input
        NodeAPI.register(self.app, route_base="/")
        self.app.run(host=ip, port=api_port)

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
        print("RECEIVED TRANSACTION")
        node.handle_transaction(transaction)
        response = {"message": "Received transaction"}
        return jsonify(response), 201

    @route("/balance", methods=["GET"])
    def get_balance(self):
        return node.blockchain.account_model.get_balances()

    @route("/stake", methods=["GET"])
    def get_stakes(self):
        return node.blockchain.get_stake_amount()

    @route("/rollback", methods=["POST"])
    def blockchain_rollback(self):
        node.handle_rollback()
        response = {"message": "Rollback performed"}
        return jsonify(response), 201

