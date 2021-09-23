"""
File: utils.py
Project: GenshinSignIn
File Created: Thursday, 23rd September 2021 8:04:23 am
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Thursday, 23rd September 2021 4:58:12 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description: 
"""

import uuid
import time
import config
import random
import string
import hashlib
import setting
import re


def generate_md5(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def split_cookies(cookies: str) -> dict:
    return dict(re.split("=", cookie.strip(), 1) for cookie in cookies.split(";"))


def get_random_text(num: int) -> str:
    return''.join(random.sample(string.ascii_lowercase + string.digits, num))


def get_timestamp(format: str = 'python') -> str:
    if format == 'python':
        return str(int(time.time()))
    return str(int(time.time()*1000))


def shake_sleep(floor: int = 2, ceil: int = 5) -> None:
    time.sleep(random.randint(floor, ceil))


def get_ds(web: bool, web_old: bool) -> str:
    if web == True:
        if web_old == True:
            n = setting.mihoyobbs_salt_web_old
        else:
            n = setting.mihoyobbs_salt_web
    else:
        n = setting.mihoyobbs_salt
    # TODO: check timestamp
    i = str(get_timestamp())
    r = get_random_text(6)
    c = generate_md5("salt=" + n + "&t=" + i + "&r=" + r)
    return f"{i},{r},{c}"


def get_device_id() -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_URL, config.Config.mihoyobbs_cookies_raw)).replace('-', '').upper()
