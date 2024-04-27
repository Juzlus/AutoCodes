#!/usr/bin/env python3

import os
import json
import asyncio

from time import sleep
from pyppeteer import launch
from datetime import datetime
from pyppeteer_stealth import stealth
from dotenv import find_dotenv, load_dotenv

timeout = 10 * 60 * 1000
selectorElement = '#promo-code-modal'
file_path_cookies = "session/cookies_keydrop.json"

reset='\033[0m'
cyan='\033[36m'
red='\033[31m'
black='\033[90m'
magenta='\033[35m'
green='\033[32m'
yellow='\033[33m'


async def lunch_website(console_mode=True):
    cookies = get_cookies()
    browser = await launch(headless=console_mode, defaultViewport=None, executablePath=os.getenv("BROWSER_PATH"))
    page = await browser.newPage()
    await stealth(page)
    await page.setUserAgent(os.getenv("CUSTOM_USER_AGENT"))
    if console_mode and cookies:
        await page.setCookie(*cookies)
    await page.goto("https://key-drop.com/")
    return [browser, page]


def get_cookies():
    f = open(file_path_cookies, 'r')
    try:
        return json.load(f)
    except:
        return None


def save_cookies(cookies):
    f = open(file_path_cookies, 'w')
    f.write(str(cookies)
            .replace('False', 'false')
            .replace('True', 'true')
            .replace("'", '"'))
    f.close()


def import_jquery(page):
    return page.evaluate('''
            var script = document.createElement('script');
            script.id = 'jquery_3_6_0';
            script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
            document.head.appendChild(script);
        ''')


def send_post(page, promo_code):
    return page.evaluate('''async function(goldenCode) {
            const url = 'https://key-drop.com/pl/apiData/Bonus/gold_activation_code';
            const jsonPayload = JSON.stringify({ promoCode: goldenCode });
    
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: url,
                    type: 'POST',
                    contentType: 'application/json',
                    data: jsonPayload,
                    success: function(data) {
                        resolve(data);
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        resolve(xhr.status);
                    }
                });
            });
        }''', promo_code)


async def keydrop_login(page):
    try:
        await page.goto("https://key-drop2.com/?q=")
        await page.waitForSelector(selectorElement, timeout=timeout)
        cookies = await page.cookies()
        save_cookies(cookies)
    except Exception:
        print(f'{black}[{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}]{reset} {red}Login timeout! (You only have 10 minutes for this){reset}')


async def check_code(page, code='KSBNMH76GF5GHJKL8'):
    await page.waitForSelector(selectorElement, timeout=timeout)
    await import_jquery(page)
    await page.waitForSelector('#jquery_3_6_0', timeout=timeout)
    sleep(2)
    result = await send_post(page, code)
    return result
