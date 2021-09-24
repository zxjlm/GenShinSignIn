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
        "bbs_signin": True,
        # 2: genshin 5: conmunity
        "bbs_signin_list": [2, 5],
        "bbs_read_posts": True,
        "bbs_like_posts": True,
        "bbs_unlike_posts": True,
        "bbs_share_posts": True,
    }
    genshin_auto_sign = True

    def __init__(self, config_path) -> None:
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        from utils import split_cookies

        with open(self.config_path, "r") as f:
            data = json.load(f)
            self.enable_config = data["enable_config"]
            self.mihoyobbs_cookies_raw = data["mihoyobbs_cookies_raw"]
            self.mihoyobbs["bbs_gobal"] = data["mihoyobbs"]["bbs_global"]
            self.mihoyobbs["bbs_signin"] = data["mihoyobbs"]["bbs_signin"]
            self.mihoyobbs["bbs_signin_list"] = data["mihoyobbs"]["bbs_signin_list"]
            self.mihoyobbs["bbs_read_posts"] = data["mihoyobbs"]["bbs_read_posts"]
            self.mihoyobbs["bbs_like_posts"] = data["mihoyobbs"]["bbs_like_posts"]
            self.mihoyobbs["bbs_unlike"] = data["mihoyobbs"]["bbs_unlike"]
            self.mihoyobbs["bbs_share"] = data["mihoyobbs"]["bbs_share"]
            self.genshin_auto_sign = data["genshin_auto_sign"]
            self.mihoyobbs_cookies = split_cookies(
                data["mihoyobbs_cookies_raw"])

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
