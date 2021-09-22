import os
import uuid
import time
import config
import random
import string
import logging
import hashlib
import setting

if os.path.exists(f"{config.path}/logging.ini"):
    logging.config.fileConfig(f"{config.path}/logging.ini")
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S')

log = logger = logging


def MD5(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def Random_text(num: int) -> str:
    return''.join(random.sample(string.ascii_lowercase + string.digits, num))


def Timestamp() -> int:
    return int(time.time())


def Get_ds(web: bool, web_old: bool) -> str:
    if web == True:
        if web_old == True:
            n = setting.mihoyobbs_Salt_web_old
        else:
            n = setting.mihoyobbs_Salt_web
    else:
        n = setting.mihoyobbs_Salt
    i = str(Timestamp())
    r = Random_text(6)
    c = MD5("salt=" + n + "&t=" + i + "&r=" + r)
    return f"{i},{r},{c}"


def Get_deviceid() -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_URL, config.mihoyobbs_Cookies)).replace(
        '-', '').upper()


def Get_item(raw_data: dict) -> str:
    temp_Name = raw_data["name"]
    temp_Cnt = raw_data["cnt"]
    return f"{temp_Name}x{temp_Cnt}"


def Nextday() -> int:
    now_time = int(time.time())
    nextday_time = now_time - now_time % 86400 + time.timezone + 86400
    return nextday_time


def Get_openssl_Version() -> int:
    try:
        import ssl
    except ImportError:
        log.error("Openssl Lib Error !!")
        # return -99
        # 建议直接更新Python的版本，有特殊情况请提交issues
        exit(-1)
    temp_List = ssl.OPENSSL_VERSION_INFO
    return int(f"{str(temp_List[0])}{str(temp_List[1])}{str(temp_List[2])}")
