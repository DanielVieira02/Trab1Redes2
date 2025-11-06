import datetime
from classes import Block
from classes import Transaction
from utils import validate_block

class Blockchain(object):
    def print_blockchain_log(self):
        current_block = self.first_block
        if current_block is None:
            return "Blockchain not initialized"
        
        accounts = {}

        while current_block != None:
            transaction = current_block.transaction
            if transaction.destiny not in accounts:
                accounts[transaction.destiny] = 0
            accounts[transaction.destiny] += transaction.amount
            if transaction.source != "":
                if transaction.source not in accounts:
                    accounts[transaction.source] = 0
                accounts[transaction.source] -= transaction.amount
            current_block = current_block.next_block
        
        print(accounts)

    def initialize_blockchain(self, initial_value: int):
        self.first_block = Block(
            Transaction(
                initial_value,
                "MiniCoins"
            ),
            datetime.datetime.now()
        )
        print("Blockchain initialized")

    def get_last_block_hash(self):
        current_block = self.first_block
        if current_block is None:
            return "Blockchain not initialized"
        
        while current_block.next_block != None:
            current_block = current_block.next_block
        
        return current_block.hash
    
    def validate_transaction(self, transaction: Transaction):
        current_block = self.first_block
        if current_block is None:
            return "Blockchain not initialized"
        
        accounts = {}

        while current_block != None:
            current_transaction = current_block.transaction
            if current_transaction.destiny not in accounts:
                accounts[current_transaction.destiny] = 0
            accounts[current_transaction.destiny] += current_transaction.amount
            if current_transaction.source != "":
                accounts[current_transaction.source] -= current_transaction.amount
            current_block = current_block.next_block

        if transaction.source not in accounts:
            return {
                "error": 1,
                "message": "Source account does not exist"
            }
        
        if accounts[transaction.source] - transaction.amount < 0:
            return {
                "error": 1,
                "message": "Source account does not have enough value"
            }

        return {
            "error": 0
        }
    
    def add_block(self, block: Block):
        current_block = self.first_block
        if current_block is None:
            return "Blockchain not initialized"
        validate = self.validate_transaction(block.transaction)
        if validate["error"] == 1:
            print(validate["message"])
            return 

        while current_block.next_block != None:
            current_block = current_block.next_block

        if not validate_block(block, current_block):
            print("Invalid block hash")
            return
        
        current_block.next_block = block