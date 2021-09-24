"""
File: config.py
Project: GenshinSignIn
File Created: Thursday, 23rd September 2021 8:04:23 am
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Thursday, 23rd September 2021 4:57:36 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description:
"""

import json
from loguru import logger


class Config:
    enable_config = True
    mihoyobbs_cookies = {}
    mihoyobbs_cookies_raw = ""
    mihoyobbs_account_id = ""
    mihoyobbs = {
        "bbs_global": True,
        # 2: genshin 5: conmunity
        "bbs_signin_list": [2, 5],
        "bbs_view_post_0": True,
        "bbs_post_up_0": True,
        "bbs_post_up_cancel": True,
        "bbs_share_posts": True,
    }
    genshin_auto_sign = True
    mail = {
        "mail_receivers": [],
        "password": "",
        "user": "",
        "host": "",
        "port": 0
    }

    def __init__(self, config_path) -> None:
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        from utils import split_cookies

        with open(self.config_path, "r") as f:
            data = json.load(f)
            self.enable_config = data["enable_config"]
            self.mihoyobbs_cookies_raw = data["mihoyobbs_cookies_raw"]
            self.genshin_auto_sign = data["genshin_auto_sign"]

            for key in self.mihoyobbs:
                self.mihoyobbs[key] = data.get('mihoyobbs', {}).get(key)
            for key in self.mail:
                self.mail[key] = data.get('mail', {}).get(key)

            if data["mihoyobbs_cookies_raw"]:
                self.mihoyobbs_cookies = split_cookies(data["mihoyobbs_cookies_raw"])

            logger.info("load config...")

    def save_config(self):
        with open(self.config_path, "r") as f:
            data = json.load(f)

        with open(self.config_path, "w") as f:
            data["mihoyobbs_cookies_raw"] = ';'.join(
                f'{k}={v}' for k, v in self.mihoyobbs_cookies.items())
            json.dump(data, f, indent=4)
            logger.info("save config...")

    def clear_cookies(self, terminate=True):
        with open(self.config_path, "r") as f:
            data = json.load(f)

        with open(self.config_path, "w") as f:
            data["mihoyobbs_cookies_raw"] = ""

            json.dump(data, f, indent=4)
            logger.info("clean config...")

        if terminate:
            logger.warning('terminate process...')
            raise SystemExit

    @classmethod
    def set_cookies_dict(cls, cookies: dict) -> None:
        cls.mihoyobbs_cookies = cookies

    @classmethod
    def get_cookies_dict(cls) -> dict:
        return cls.mihoyobbs_cookies
