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

class Block(object):
    def __init__(self, transaction: Transaction, timestamp: datetime, previous_hash: string = ""):
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash = "0"
        self.nonce = random.randint(0, sys.maxsize)
        self.next_block = None
        while self.hash[:3] != '038':
            self.nonce = self.nonce + 1
            self.hash = calculate_block_hash(self, transaction)