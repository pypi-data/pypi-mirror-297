#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Copyright 2020 by kiutra GmbH
# All rights reserved.
# This file is part of Kiutra-API,
# and is released under the "Apache Version 2.0 License". Please see the LICENSE
# file that should have been included as part of this package.

import asyncio
import json
import queue
import time

import websockets
import sys
from enum import Enum
from collections import deque

update_queue = queue.Queue() # deque(maxlen=100)

class MessageCategory(Enum):
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'
    BUFFERED = 'buffered'
    UPDATE = 'update'
    INSTRUCTION = 'instruction'

async def main(client_address="ws://192.168.11.20:8008"):
    """
    Print client that receives and prints kiutra messages broadcast using a websocket on port 8008

    Args:
        client_address:

    Returns:

    """
    async for websocket in websockets.connect(client_address):
        try:
            await websocket.send(json.dumps({"type": "init", "message": "trying to connect"}))
        except websockets.ConnectionClosed:
            continue
        else:
            while True:
                message = None
                try:
                    message = await websocket.recv()
                    msg_json = json.loads(message)
                    update_queue.put(msg_json)
                except websockets.ConnectionClosed:
                    print("Connection Closed")
                    break
                except json.decoder.JSONDecodeError:
                    break
                except KeyError:
                    print(message, sys.exc_info())
            continue

async def handle_update_queue():
    while True:
        while True:
            try:
                entry = update_queue.get(False)
                category = entry["message"]["message"]["category"]
                if category == MessageCategory.ERROR.name.lower():
                    icon = '\u2716'
                elif category == MessageCategory.SUCCESS.name.lower():
                    icon = '\u2713'
                elif category == MessageCategory.WARNING.name.lower():
                    icon = '\u26A0'
                elif category == MessageCategory.INFO.name.lower():
                    icon = '\u24D8'
                elif category == MessageCategory.UPDATE.name.lower():
                    icon = '\u27f2'
                else:
                    icon = f'### {category} ###'
                print(f'{icon} {entry["message"]["origin"]}:{entry["message"]["timestamp"]}$  {entry["message"]["message"]["text"]}')
                data = entry["message"]["message"]["data"]
                if data:
                    print(f'{data}')
            except (IndexError, queue.Empty):
                break
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    client_address = "ws://192.168.0.13:8008"
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(main(client_address), handle_update_queue()))
    except (KeyboardInterrupt, BrokenPipeError, SystemExit):
        sys.exit(0)
