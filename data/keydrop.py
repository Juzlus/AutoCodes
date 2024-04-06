#!/usr/bin/env python3

import json
import asyncio

from time import sleep
from pyppeteer import launch
from datetime import datetime
from pyppeteer_stealth import stealth

file_path_cookies = "session/cookies_keydrop.json"


async def lunch_website(console_mode=True):
    browser = await launch(headless=console_mode, defaultViewport=None)
    page = await browser.newPage()
    await stealth(page)
    return [browser, page]


def get_cookies():
    f = open(file_path_cookies, 'r')
    cookies = json.load(f)
    return cookies


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
    response = page.evaluate('''async function(goldenCode) {
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
    return response


async def check_code(code):
    [browser, page] = await lunch_website()
    cookies = get_cookies()
    await page.setCookie(*cookies)
    await page.goto("https://key-drop.com/")
    try:
        await page.waitForSelector('#confirm-login-modal')
        await import_jquery(page)
        await page.waitForSelector('#jquery_3_6_0')
        sleep(2)
        code_response = await send_post(page, code or "KSBNMH76GF5GHJKL8")
        if code_response['errorCode'] == 'notLoggedIn':
            raise Exception('notLoggedIn')
    except Exception:
        print('Your cookies expired!')
        await browser.close()
        await keydrop_login()
        return False
    if not code:
        print('Success')
    else:
        if code_response['status']:
            print(f'{datetime.now()} | {code} | {code_response["goldBonus"]} Gold')
        else:
            print(f'{datetime.now()} | {code} | {code_response["errorCode"]} - {code_response["info"]}')
    await browser.close()
    return True


async def keydrop_login():
    [browser, page] = await lunch_website(False)
    await page.goto("https://key-drop.com/")
    try:
        await page.goto("https://key-drop2.com/?q=")
        await page.waitForSelector('#promo-code-modal', timeout=10 * 60 * 1000)
        cookies = await page.cookies()
        save_cookies(cookies)
        print('Configuration successful!')
    except Exception:
        print('Login timeout! (You only have 10 minutes for this)')
    await browser.close()


def run_check_code(golden_code=None):
    asyncio.get_event_loop().run_until_complete(check_code(golden_code))
