import datetime
from blockchain import Blockchain
from classes import Block, Transaction

blockchain = Blockchain()
blockchain.initialize_blockchain(200)

second_transaction = Transaction(
    50,
    "Daniel",
    "MiniCoins"
)

second_block = Block(
    second_transaction,
    datetime.datetime.now(),
    blockchain.get_last_block_hash()
)

blockchain.add_block(second_block)

third_transaction = Transaction(
    75,
    "MiniCoins",
    "Breno"
)

third_block = Block(
    third_transaction,
    datetime.datetime.now(),
    blockchain.get_last_block_hash()
)

blockchain.add_block(third_block)

transaction = Transaction(
    25,
    "MiniCoins",
    "Daniel"
)

block = Block(
    transaction,
    datetime.datetime.now(),
    blockchain.get_last_block_hash()
)

blockchain.add_block(block)

blockchain.print_blockchain_log()