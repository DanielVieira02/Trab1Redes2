#!/usr/bin/env python

import asyncio
import datetime
import json
import logging
import os
import time
import settings
import sys

from websockets.asyncio.client import connect
from classes import Block, Transaction

user_name = ""

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

    last_hash = await get_last_hash_from_blockchain(websocket)
    result = await send_block_to_blockchain(websocket, user_name, amount, "MiniCoins", last_hash)
    print(result)

async def deposit(websocket):
    os.system('cls' if os.name == 'nt' else 'clear')
    amount = int(input("Insira a quantidade do depósito: "))

    last_hash = await get_last_hash_from_blockchain(websocket)
    result = await send_block_to_blockchain(websocket, "MiniCoins", amount, user_name, last_hash)
    
    if result['status'] == "success":
        print("Depósito realizado com sucesso")
    else:
        print("Falha ao tentar realizar depósito")
        print(result['message'])

async def transfer(websocket):
    os.system('cls' if os.name == 'nt' else 'clear')
    amount = int(input("Insira a quantidade da transferência: "))
    destiny = input("Insira o destino do saque: ")

    last_hash = await get_last_hash_from_blockchain(websocket)
    result = await send_block_to_blockchain(websocket, destiny, amount, user_name, last_hash)
    print(result)

async def verify_blockchain(websocket):
    os.system('cls' if os.name == 'nt' else 'clear')
    request = {
        "type": settings.REQUEST_VERIFY_BLOCKCHAIN,
    }

    print("ow")
    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    print(response["message"])


async def client_routine():
    uri = "ws://127.0.0.1:8038"
    
    if len(sys.argv) > 1:
        uri = "ws://" + sys.argv[1] + ":8038"

    user_input = 1
    async with connect(uri) as websocket:
        while user_input != "0":
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("|-| [1] - Sacar")
                print("|-| [2] - Depositar")
                print("|-| [3] - Transferir")
                print("|-| [4] - Verificar blockchain")
                print("|-| [0] - Encerrar\n")

                user_input = input("Insira uma opção: ")

                match user_input:
                    case "1":
                        await withdraw(websocket)
                    case "2":
                        await deposit(websocket)
                    case "3":
                        await transfer(websocket)
                    case "4":
                        await verify_blockchain(websocket)
                    case "0":
                        print("Encerrando programa...")
                    case _:
                        print("Opção inválida")

                time.sleep(1.5)
            except Exception as e:
                logging.error('Error at %s', 'division', exc_info=e)
                continue

if __name__ == "__main__":
    user_name = input("Para começar, insira seu nome de usuário: ")
    asyncio.run(client_routine())