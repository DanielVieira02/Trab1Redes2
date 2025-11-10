#!/usr/bin/env python

import asyncio
import json
import classes
import settings

from blockchain import Blockchain
from classes import Block, Transaction
from websockets.asyncio.server import serve

blockchain = Blockchain()
blockchain.initialize_blockchain(200)

async def server_routine(websocket):
    blockchain.print_blockchain_log()
    async for message in websocket:
        event = json.loads(message)
        request_type = event["type"]

        try:
            match request_type:
                case settings.REQUEST_BLOCKCHAIN_HASH:
                    response = {
                        "status": "success",
                        "hash": blockchain.get_last_block_hash()
                    }
                case settings.REQUEST_ADD_BLOCK:
                    block = classes.rebuild_block(event['block'])
                    if blockchain.add_block(block) == 0:
                        response = {
                            "status": "success"
                        }
                    else:
                        response = {
                            "status": "error"
                        }                        
                case _:
                    response = {
                        "status": "no_match_request_found",
                    }
        except Exception as e:
            response = {
                "code": "status"
            }
            print(repr(e))
            await websocket.send(json.dumps(response))
            continue

        await websocket.send(json.dumps(response))



async def main():
    async with serve(server_routine, "localhost", 8038) as server:
        blockchain.print_blockchain_log()
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())