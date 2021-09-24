"""
File: genshin.py
Project: GenshinSignIn
File Created: Thursday, 23rd September 2021 8:04:23 am
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Thursday, 23rd September 2021 4:57:45 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description:
"""

import utils
from config import Config
import setting
import requests
from loguru import logger


class Genshin:
    def __init__(self, cfg: Config) -> None:
        self.s = requests.session()
        self.cfg = cfg
        self.s.headers = {
            'Accept': 'application/json, text/plain, */*',
            'DS': utils.get_ds(web=True, web_old=True),
            'Origin': 'https://webstatic.mihoyo.com',
            'x-rpc-app_version': setting.mihoyobbs_version_old,
            'User-Agent': ('Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.3.0'),
            'x-rpc-client_type': setting.mihoyobbs_client_type_web,
            'Referer': ('https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id='
                        'e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon'),
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.mihoyo.hyperion',
            'x-rpc-device_id': utils.get_device_id()
        }
        self.s.cookies.update(self.cfg.mihoyobbs_cookies)
        self.verify = False
        self.refresh_cookies()

        self.accounts = self.get_accounts()
        if len(self.accounts) != 0:
            self.sign_awards = self.get_sign_awards()

    def get_accounts(self) -> list:
        logger.info("get account list...")
        result = []
        response = self.s.get(setting.genshin_account_info_url)
        data = response.json()
        if data["retcode"] != 0:
            logger.warning("get account list failed")
            raise SystemExit
        for single_data in data["data"]["list"]:
            result.append({
                'nickname': single_data["nickname"],
                'game_uid': single_data["game_uid"],
                'region': single_data["region"]
            })
        logger.info(f"get {len(result)} accounts")
        return result

    def get_sign_awards(self) -> list:
        logger.info("get sign in awards...")
        response = self.s.get(setting.genshin_signed_url.format(
            setting.genshin_act_id))
        data = response.json()
        if data["retcode"] != 0:
            logger.warning("get sgin awards failed")
            raise SystemExit
        return data["data"]["awards"]

    def refresh_cookies(self):
        logger.info('---------------> start to refresh genshin cookies.')
        params = (
            ('stoken', self.cfg.mihoyobbs_cookies['stoken']),
            ('uid', self.cfg.mihoyobbs_cookies['stuid']),
        )
        response_cookie = self.s.get(setting.genshin_cookie_refresh, params=params)
        self.s.cookies.update({'account_id': self.cfg.mihoyobbs_cookies['stuid'],
                              'cookie_token': response_cookie.json()['data']['cookie_token']})
        logger.success('<------------------- refresh genshin cookies succeed.')

    def is_signed(self, region: str, uid: str):
        url = setting.genshin_is_sign_url.format(
            setting.genshin_act_id, region, uid)
        response = self.s.get(url)
        data = response.json()
        if data["retcode"] != 0:
            logger.warning("get account sign in info failed")
            raise SystemExit
        return data["data"]

    @staticmethod
    def get_item(raw_data: dict) -> str:
        return f'{raw_data["name"]}x{raw_data["cnt"]}'

    def sign_account(self, account):
        logger.info(f"now sign in for account {account['nickname']}...")

        signed_data = self.is_signed(
            region=account['region'], uid=account['game_uid'])

        if signed_data["first_bind"]:
            logger.warning(f"{account['nickname']} manual sign first")
        else:
            sign_days = signed_data["total_sign_day"] - 1
            if signed_data["is_sign"]:
                logger.info(
                    f"{account['nickname']} has signed~ award today is {self.get_item(self.sign_awards[sign_days])}")
            else:
                utils.shake_sleep()
                post_data = {'act_id': setting.genshin_act_id, 'region': account['region'], 'uid': account['game_uid']}
                response = self.s.post(url=setting.genshin_sign_url, json=post_data)
                data = response.json()
                if data["retcode"] == 0:
                    if sign_days == 0:
                        logger.info(
                            f"{account['nickname']} sign in succeed~ award today is {self.get_item(self.sign_awards[sign_days])}")
                    else:
                        logger.info(
                            f"{account['nickname']} sign in succeed~ award today is {self.get_item(self.sign_awards[sign_days + 1])}")
                elif data["retcode"] == -5003:
                    logger.info(
                        f"{account['nickname']} has signed~ award today is {self.get_item(self.sign_awards[sign_days])}")
                else:
                    logger.warning(f"sign in failed, response: {data}")

    def main(self):
        if not self.accounts:
            logger.warning("no target account")
            return

        for account in self.accounts:
            self.sign_account(account)
