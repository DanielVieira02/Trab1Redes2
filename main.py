#!/usr/bin/env python

import asyncio

from blockchain import Blockchain
from classes import Block, Transaction
from websockets.asyncio.server import serve

blockchain = Blockchain()
blockchain.initialize_blockchain(200)

async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def main():
    async with serve(hello, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())