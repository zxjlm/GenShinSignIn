"""
File: login.py
Project: GenshinSignIn
File Created: Thursday, 23rd September 2021 8:04:23 am
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Thursday, 23rd September 2021 4:57:50 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description: 
"""

from typing import Union
from utils import get_timestamp, split_cookies
from config import Config
import requests
import setting
from loguru import logger
from playwright.async_api import async_playwright
import asyncio


async def simulator(return_type='dict') -> Union[dict, str]:
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(setting.mihoyo_login_url)
        async with page.expect_navigation(url='*/account/home', timeout=0) as first:
            await asyncio.sleep(5)

        cookies = await context.cookies()
        await context.close()
        await browser.close()
    if return_type == 'dict':
        return {cookie['name']: cookie['value'] for cookie in cookies}
    elif return_type == 'str':
        return ';'.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    else:
        raise Exception('invalid cookie type, must be str or dict')


class Login:
    _headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'Accept': 'application/json, text/plain, */*',
        'x-rpc-device_id': '0b147691-d288-4284-8b1d-c0a613ece44b',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'x-rpc-client_type': '4',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://user.mihoyo.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://user.mihoyo.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
    }

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.use_simulator = True

    def is_cookies_expires(self) -> bool:
        params = (
            ('t', get_timestamp('js')),
        )
        headers = self._headers.copy()
        headers['Cookie'] = self.cfg.mihoyobbs_cookies_raw
        response = requests.get('https://webapi.account.mihoyo.com/Api/login_by_cookie',
                                headers=headers, params=params)
        if response.json()['data']['msg'] == '登录信息已失效，请重新登录':
            logger.warning('login cookie expires!!!')
            return True
        logger.success(
            f'account_email: {response.json()["data"]["account_info"]["email"]}, login cookie is effect~')
        return False

    def resolve_cookies(self) -> None:
        logger.info('now start to set login_ticket, (1/3)')
        self.cfg.mihoyobbs_login_ticket = self.cfg.mihoyobbs_cookies['login_ticket']

        logger.info('now start to set stuid, (2/3)')
        response = requests.get(url=setting.bbs_cookie_url.format(
            self.cfg.mihoyobbs_login_ticket))
        data = response.json()
        if "成功" in data["data"]["msg"]:
            self.cfg.mihoyobbs_stuid = str(
                data["data"]["cookie_info"]["account_id"])

            logger.info('now start to set stoken, (3/3)')
            response = requests.get(url=setting.bbs_cookie_url2.format(
                self.cfg.mihoyobbs_login_ticket, self.cfg.mihoyobbs_stuid))
            data = response.json()
            self.cfg.mihoyobbs_stoken = data["data"]["list"][0]["token"]

            logger.success("login succeed")
            self.cfg.save_config()
        else:
            logger.error("get stuid failed")
            self.cfg.clear_cookies()

    def cookie_process(self) -> None:
        if not self.cfg.mihoyobbs_cookies_raw or self.is_cookies_expires():
            self.cfg.clear_cookies()
            if self.use_simulator:
                logger.info(
                    '--------------> now use simulator browser to get cookie.')
                self.cfg.mihoyobbs_cookies = asyncio.run(simulator())
                self.cfg.mihoyobbs_cookies_raw = ';'.join(
                    f'{k}={v}' for k, v in self.cfg.mihoyobbs_cookies.items())
                logger.success('<----------------- get cookie succeed')
            else:
                # TODO: 进行通知
                raise SystemExit

            if not self.cfg.mihoyobbs_cookies:
                self.cfg.mihoyobbs_cookies = split_cookies(
                    self.cfg.mihoyobbs_cookies_raw)

            if self.cfg.mihoyobbs_cookies.get('login_ticket'):
                self.resolve_cookies()
            else:
                logger.error("login_ticket not in cookie")
                self.cfg.clear_cookies()


if __name__ == "__main__":
    cookies = asyncio.run(simulator(return_type='str'))
    print(cookies)
