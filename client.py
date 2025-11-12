#!/usr/bin/env python

import asyncio
import datetime
import json
import os
import time
import settings

from websockets.asyncio.client import connect
from classes import Block, Transaction

async def get_last_hash_from_blockchain(websocket):
    request = {
        "type": settings.REQUEST_BLOCKCHAIN_HASH
    }
    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    response = json.loads(response)

    hash = response['hash']
    assert hash
    return hash

async def send_block_to_blockchain(websocket, destiny, amount, source, last_hash):
    transaction = Transaction(amount, destiny, source)
    block = Block(transaction, datetime.datetime.now(), last_hash)

    request = {
        "type": settings.REQUEST_ADD_BLOCK,
        "block": block.to_json(),
    }

    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    return json.loads(response)

async def withdraw(websocket):
    os.system('cls' if os.name == 'nt' else 'clear')
    amount = int(input("Insira a quantidade a sacar: "))
    destiny = input("Insira o destino do saque: ")

    last_hash = await get_last_hash_from_blockchain(websocket)
    result = await send_block_to_blockchain(websocket, destiny, amount, "MiniCoins", last_hash)
    print(result)

async def deposit(websocket):
    os.system('cls' if os.name == 'nt' else 'clear')
    amount = int(input("Insira a quantidade da transferência: "))
    source = input("Insira a origem do saque: ")
    destiny = input("Insira o destino do saque: ")

    last_hash = await get_last_hash_from_blockchain(websocket)
    result = await send_block_to_blockchain(websocket, destiny, amount, source, last_hash)
    print(result)

async def client_routine():
    uri = "ws://localhost:8038"
    user_input = 1
    async with connect(uri) as websocket:
        while user_input != 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("|-| [1] - Sacar")
            print("|-| [2] - Depositar")
            print("|-| [3] - Verificar blockchain")
            print("|-| [0] - Encerrar\n")

            user_input = input("Insira uma opção: ")

            match user_input:
                case "1":
                    await withdraw(websocket)
                case "2":
                    await deposit(websocket)
                case "3":
                    print("Blockchain verídica")
                case "0":
                    print("Encerrando programa...")
                case _:
                    print("Opção inválida")

            time.sleep(1.5)

if __name__ == "__main__":
    asyncio.run(client_routine())