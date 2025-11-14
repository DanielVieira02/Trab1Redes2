import random
import string

import datetime
import sys

from utils import calculate_block_hash

class Transaction(object):
    def __init__(self, amount: int, destiny: int, source: string = ""):
        self.amount = amount
        self.destiny = destiny
        self.source = source

    def to_json(self):
        return {
            "amount": self.amount,
            "destiny": self.destiny,
            "source": self.source,
        }

class Block(object):
    def __init__(self, transaction: Transaction, timestamp: datetime, previous_hash: string = "", initialize_hash = True):
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash = "0"
        self.nonce = random.randint(0, sys.maxsize)
        self.next_block = None
        while self.hash[:3] != '038' and initialize_hash:
            self.nonce = self.nonce + 1
            self.hash = calculate_block_hash(self, transaction)

    def to_json(self):
        return {
            "transaction": self.transaction.to_json(),
            "previous_hash": self.previous_hash,
            "timestamp": str(self.timestamp),
            "hash": self.hash,
            "nonce": self.nonce
        }
    
def rebuild_block(block):
        transaction = Transaction(block['transaction']['amount'], block['transaction']['destiny'], block['transaction']['source'])
        new_block = Block(transaction, block['timestamp'], block['previous_hash'], False)
        new_block.nonce = block['nonce']
        new_block.hash = block['hash']
        return new_block