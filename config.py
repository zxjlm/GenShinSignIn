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
from functools import reduce
import setting


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
        "bbs_share_post_0": True,
    }
    genshin_auto_sign = True
    mail = {
        "receivers": [],
        "password": "",
        "user": "",
        "host": "",
        "port": 0
    }

    def __init__(self, config_path: str, auto_load=True) -> None:
        """初始化配置, 将会自动从配置文件的路径中读取

        Args:
            config_path (str): 配置文件的路径
            auto_load (bool, optional): 是否自动加载配置文件到类变量. Defaults to True.
        """
        self.config_path = config_path
        if auto_load:
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

    def validate_config_table_row(self, columns):
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        result = []

        for col in columns:
            col_path_list = col.split('.')
            judge = reduce(lambda x, y: x.get(y, {}), [config, *col_path_list])
            result.append('√' if judge else 'x')
        return result

    def validate_config_file(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        if config.get('enable_config', False):
            logger.success('config is enable')
            if config.get("mihoyobbs_cookies_raw"):
                logger.warning('cookies is empty, maybe you can use --parser-cookie to generate a cookie.')

            mail = config.get('mail', {})
            if receivers := mail.get('receivers'):
                if reduce(lambda x, y: x and y, mail.values()):
                    logger.success('mail is enable, receivers: {}, '
                                   'config about mail all have been filled', receivers)
                else:
                    logger.warning('mail is enable, receivers: {}, '
                                   'but mail config about mail need to be filled', receivers)
            else:
                logger.info('mail is disable')

            mihoyobbs = config.get('mihoyobbs', {})
            if mihoyobbs.get('bbs_global'):
                logger.success('bbs function is enable.')
                if mihoyobbs.get('bbs_signin') and (sign_list := mihoyobbs.get('bbs_signin_list', [])):
                    sign_name_list = [foo["name"] for foo in setting.mihoyobbs_list if foo['id'] in sign_list]
                    logger.info('    -> sign function is enable, sign list: {}.', sign_name_list)
                if mihoyobbs.get('bbs_view_post_0'):
                    logger.info('    -> view post is enable.')
                if mihoyobbs.get('bbs_post_up_0'):
                    logger.info('    -> up post is enable.')
                    if mihoyobbs.get('bbs_post_up_cancel'):
                        logger.info('        -> cancel up post is enable.')
                if mihoyobbs.get('bbs_share_post_0'):
                    logger.info('    -> share post is enable.')
            else:
                logger.info('bbs function is disable.')

        else:
            logger.info('config is disable')

    @classmethod
    def set_cookies_dict(cls, cookies: dict) -> None:
        cls.mihoyobbs_cookies = cookies

    @classmethod
    def get_cookies_dict(cls) -> dict:
        return cls.mihoyobbs_cookies
