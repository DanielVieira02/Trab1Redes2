#!/usr/bin/env python

import datetime
import json
from websockets.sync.client import connect

from classes import Block, Transaction
import settings

def hello():
    uri = "ws://localhost:8038"
    with connect(uri) as websocket:
        request = {
            "type": settings.REQUEST_BLOCKCHAIN_HASH
        }

        websocket.send(json.dumps(request))
        print(f">>> {request['type']}")

        response = json.loads(websocket.recv())
        print(f"<<< {response['hash']}")

        last_hash = response['hash']

        transaction = Transaction(50, "Daniel", "MiniCoins")
        block = Block(transaction, datetime.datetime.now(), last_hash)

        request = {
            "type": settings.REQUEST_ADD_BLOCK,
            "block": block.to_json()
        }

        websocket.send(json.dumps(request))

if __name__ == "__main__":
    hello()