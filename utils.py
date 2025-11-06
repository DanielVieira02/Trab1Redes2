from hashlib import sha256

def validate_block(block, previous_block):
    return (block.previous_hash == previous_block.hash
            and block.hash == calculate_block_hash(block, block.transaction)
            and block.hash[:3] == "038")

def calculate_block_hash(block, transaction):
        data = "AMT" + str(transaction.amount) + "DTN" + transaction.destiny + "SRC" + transaction.source
        data_to_hash = block.previous_hash + str(block.timestamp) + str(block.nonce) + data
        sha = sha256(data_to_hash.encode())
        bytes = sha.hexdigest()

        return str(bytes)