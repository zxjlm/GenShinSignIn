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
    mihoyobbs_login_ticket = ""
    mihoyobbs_stuid = ""
    mihoyobbs_stoken = ""
    mihoyobbs_cookies = {}
    mihoyobbs_cookies_raw = ""
    mihoyobbs_account_id = ""
    mihoyobbs = {
        "bbs_global": True,
        "bbs_signin": True,
        "bbs_signin_multi": True,
        # 1: honkai3rd 2: genshin 3: honkai2 4: shijian 5: main conmunity
        "bbs_signin_multi_list": [2, 5],
        "bbs_read_posts": True,
        "bbs_like_posts": True,
        "bbs_unlike_posts": True,
        "bbs_share_posts": True,
    }
    genshin_auto_sign = True
    honkai3rd_auto_sign = True

    def __init__(self, config_path) -> None:
        self.config_path = config_path

    def load_config(self):
        with open(self.config_path, "r") as f:
            data = json.load(f)
            self.enable_config = data["enable_config"]
            self.mihoyobbs_login_ticket = data["mihoyobbs_login_ticket"]
            self.mihoyobbs_stuid = data["mihoyobbs_stuid"]
            self.mihoyobbs_stoken = data["mihoyobbs_stoken"]
            # self.mihoyobbs_cookies_raw = data["mihoyobbs_cookies_raw"]
            self.mihoyobbs["bbs_gobal"] = data["mihoyobbs"]["bbs_global"]
            self.mihoyobbs["bbs_signin"] = data["mihoyobbs"]["bbs_signin"]
            self.mihoyobbs["bbs_signin_multi"] = data["mihoyobbs"]["bbs_signin_multi"]
            self.mihoyobbs["bbs_signin_multi_list"] = data["mihoyobbs"]["bbs_signin_multi_list"]
            self.mihoyobbs["bbs_read_posts"] = data["mihoyobbs"]["bbs_read_posts"]
            self.mihoyobbs["bbs_like_posts"] = data["mihoyobbs"]["bbs_like_posts"]
            self.mihoyobbs["bbs_unlike"] = data["mihoyobbs"]["bbs_unlike"]
            self.mihoyobbs["bbs_share"] = data["mihoyobbs"]["bbs_share"]
            self.genshin_auto_sign = data["genshin_auto_sign"]

            logger.info("Config加载完毕")

    def save_config(self):
        with open(self.config_path, "r+") as f:
            data = json.load(f)
            data["mihoyobbs_Login_ticket"] = self.mihoyobbs_Login_ticket
            data["mihoyobbs_Stuid"] = self.mihoyobbs_Stuid
            data["mihoyobbs_Stoken"] = self.mihoyobbs_Stoken
            json.dump(data, f, sort_keys=False, ensure_ascii=False,
                      indent=4, separators=(', ', ': '))
            logger.info("Config保存完毕")

    def clear_cookies(self):
        with open(self.config_path, "r+") as f:
            data = json.load(f)
            data["mihoyobbs_login_ticket"] = ""
            data["mihoyobbs_stuid"] = ""
            data["mihoyobbs_stoken"] = ""
            data["mihoyobbs_cookies"] = ""

            json.dump(data, f, sort_keys=False,
                      indent=4, separators=(', ', ': '))
            logger.info("Cookie删除完毕")
