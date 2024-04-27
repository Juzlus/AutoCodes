#!/usr/bin/env python3

import os
import re
import psutil
import signal
import asyncio

import keydrop
from datetime import datetime
from dotenv import find_dotenv, load_dotenv
from telethon import TelegramClient, events

reset='\033[0m'
cyan='\033[36m'
red='\033[31m'
black='\033[90m'
magenta='\033[35m'
green='\033[32m'
yellow='\033[33m'

used_codes = []
codes = []

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

browser = None
page = None


def get_channels_id():
    channels_id = []
    for el in os.getenv("CHANNELS_ID").strip().split(","):
        channels_id.append(int(el))
    return channels_id


def get_golden_code_from_text(text):
    args = text.split()
    for arg in args:
        if len(arg) == 17:
            golden_code = arg.upper()
            if re.compile(r'^[A-Z0-9]+$').match(golden_code):
                if golden_code not in used_codes:
                    used_codes.append(golden_code)
                    codes.append(golden_code)
    return


async def queue(page):
    if len(codes) == 0:
        return
    golden_code = codes[0]
    codes.pop(0)
    code_response = await keydrop.check_code(page, golden_code)
    if code_response['status']:
        print(f'{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} {green}{golden_code} - {code_response["goldBonus"]} Gold{reset}')
    else:
        print(f'{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} {red}{golden_code} - {code_response["errorCode"]} - {code_response["info"]}{reset}')
    await asyncio.sleep(10)
    await queue(page)


async def closeOldBrowser():
    f = open('session//pids.txt', 'r+')
    for line in f.readlines():
        try:
            pid = int(line)
            process = psutil.Process(pid)
            if process:
                if "chrome" in process.name().lower():
                    os.kill(pid, signal.SIGTERM)
        except:
            pass
    f.truncate(0)
    f.close()


async def connecting():
    print(f'{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} Connecting to servers...')

    print(f'{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} Connecting to the {magenta}Telegram{reset} account: ', end='')
    client = TelegramClient('session/session_telegram', int(os.getenv("API_ID")), os.getenv("API_HASH"))

    if not client:
        raise Exception('Failed')

    print(f'{green}Success')
    await client.start()

    print(f'{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} Connecting to the {magenta}key-drop{reset} account: ', end='')

    [browser, page] = await keydrop.lunch_website()
    code_response = await keydrop.check_code(page)

    if not code_response:
        raise Exception('Failed to connect to Keydrop!')

    if code_response == 403 or code_response['errorCode'] == 'notLoggedIn':
        print(f'{yellow}Your cookies expired!')
        await browser.close()
        [browser, page] = await keydrop.lunch_website(False)
        await keydrop.keydrop_login(page)
        code_response = await keydrop.check_code(page)
        await browser.close()
        if code_response == 403 or code_response['errorCode'] == 'notLoggedIn':
            print(f'{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} ', end='')
            raise Exception('Failed')
        print(f'{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} {green}Configuration successful!{reset}')
        [browser, page] = await keydrop.lunch_website()
    else:
        print(f'{green}Success')
    print(f'\n{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} Waiting for new golden codes...')

    @client.on(events.NewMessage(chats=get_channels_id()))
    async def my_event_handler(event):
        text = event.raw_text
        if len(codes) == 0:
            get_golden_code_from_text(text)
            await queue(page)
        else:
            get_golden_code_from_text(text)
    await client.run_until_disconnected()


async def main():
    try:
        await connecting()
    except Exception as e:
        print(f'{red}{e}{reset}')


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.run(closeOldBrowser())
    try:
        loop.run_until_complete(main())
    except Exception:
        pass
