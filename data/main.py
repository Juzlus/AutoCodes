#!/usr/bin/env python3

import os
import asyncio

import keydrop
from dotenv import find_dotenv, load_dotenv
from telethon import TelegramClient, events

used_codes = {}
codes = []

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


def get_channels_id():
    channels_id = []
    for el in os.getenv("CHANNELS_ID").strip().split(","):
        channels_id.append(int(el))
    return channels_id


def get_golden_code_from_text(text):
    args = text.split()
    for arg in args:
        if len(arg) == 17:
            if not used_codes.get(arg.upper()):
                used_codes[arg.upper()] = True
                codes.append(arg.upper())
    return


async def queue():
    if len(codes) == 0:
        return
    golden_code = codes[0]
    codes.pop(0)
    await keydrop.check_code(golden_code)
    await asyncio.sleep(10)
    await queue()


def connecting():
    print("Connecting to the Key-drop.com account: ", end='')
    keydrop.run_check_code()

    client = TelegramClient('session/session_telegram', int(os.getenv("API_ID")), os.getenv("API_HASH"))
    print("Connecting to the Telegram account: ", end='')
    client.start()
    print("Success")
    print('\nWaiting for new golden codes...')

    @client.on(events.NewMessage(chats=get_channels_id()))
    async def my_event_handler(event):
        text = event.raw_text
        if len(codes) == 0:
            get_golden_code_from_text(text)
            await queue()
        else:
            get_golden_code_from_text(text)
    client.run_until_disconnected()


if __name__ == "__main__":
    connecting()
