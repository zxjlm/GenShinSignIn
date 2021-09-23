"""
File: mihoyobbs.py
Project: GenshinSignIn
File Created: Thursday, 23rd September 2021 8:04:23 am
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Thursday, 23rd September 2021 4:57:59 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description:
"""

import utils
from config import Config
import random
import setting
import requests
from loguru import logger


class MihoyoBBS:
    can_get_points = 0
    already_received_points = 0
    total_points = 0

    def __init__(self, cfg: Config):
        self.s = requests.Session()
        self.s.headers = {
            "DS": utils.get_ds(web=False, web_old=False),
            "cookie": f"stuid={cfg.mihoyobbs_stuid};stoken={cfg.mihoyobbs_stoken}",
            "x-rpc-client_type": setting.mihoyobbs_client_type,
            "x-rpc-app_version": setting.mihoyobbs_version,
            "x-rpc-sys_version": "6.0.1",
            "x-rpc-channel": "mihoyo",
            "x-rpc-device_id": utils.get_device_id(),
            "x-rpc-device_name": utils.get_random_text(random.randint(1, 10)),
            "x-rpc-device_model": "Mi 10",
            "Referer": "https://app.mihoyo.com",
            "Host": "bbs-api.mihoyo.com",
            "User-Agent": "okhttp/4.8.0"
        }
        self.s.cookies.update(cfg.mihoyobbs_cookies)
        self.s.verify = False

        self.task_do = {
            "bbs_sign": False,
            "bbs_read_posts": False,
            "bbs_read_posts_num": 3,
            "bbs_like_posts": False,
            "bbs_like_posts_num": 5,
            "bbs_share": False
        }
        self.get_tasks()
        if self.task_do["bbs_read_posts"] and self.task_do["bbs_like_posts"] and self.task_do["bbs_share"]:
            pass
        else:
            self.posts = self.get_posts()

    def get_tasks(self):
        logger.info("start to get tasks.")
        response = self.s.get(url=setting.bbs_tasks_list)
        data = response.json()
        if "err" in data["message"]:
            logger.info(
                "get tasks failed, maybe cookie need to renew, data: {}", data)
            # Config().clear_cookies()
            raise SystemExit
        else:
            self.today_get_coins = data["data"]["can_get_points"]
            self.today_have_getcoins = data["data"]["already_received_points"]
            self.total_points = data["data"]["total_points"]
            if self.today_get_coins == 0:
                self.task_do["bbs_sign"] = True
                self.task_do["bbs_read_posts"] = True
                self.task_do["bbs_like_posts"] = True
                self.task_do["bbs_share"] = True
            else:
                if data["data"]["states"][0]["mission_id"] >= 62:
                    logger.info(
                        f"{self.today_get_coins} miyo-coin can be getten.")
                else:
                    logger.info(
                        f"rest task not finished,{self.today_get_coins} miyo-coin can be getten.")
                    for state in data["data"]["states"]:
                        if state["mission_id"] == 58:
                            if state["is_get_award"]:
                                self.task_do["bbs_sign"] = True
                        elif state["mission_id"] == 59:
                            if state["is_get_award"]:
                                self.task_do["bbs_read_posts"] = True
                            else:
                                self.task_do["bbs_read_posts_num"] -= state["happened_times"]
                        elif state["mission_id"] == 60:
                            if state["is_get_award"]:
                                self.task_do["bbs_like_posts"] = True
                            else:
                                self.task_do["bbs_like_posts_num"] -= state["happened_times"]
                        elif state["mission_id"] == 61:
                            if state["is_get_award"]:
                                self.task_do["bbs_share"] = True
                                break

    def get_posts(self) -> list:
        logger.info("get posts......")
        result = []
        response = self.s.get(url=setting.bbs_list_url.format(
            setting.mihoyobbs_list_use[0]["forumId"]))
        data = response.json()
        for i in range(self.task_do['bbs_like_posts_num']):
            result.append({
                'post_id': data["data"]["list"][i]["post"]["post_id"],
                'subject': data["data"]["list"][i]["post"]["subject"]
            })
        logger.info("get {} posts".format(len(result)))
        return result

    def sign_in_bbs(self):
        if self.task_do["bbs_sign"]:
            logger.info("~")
        else:
            logger.info("start to sign in......")
            for i in setting.mihoyobbs_list_use:
                response = self.s.post(url=setting.bbs_sign_url.format(
                    i["id"]), data="")
                data = response.json()
                if data["message"] == 'OK':
                    logger.info(str(i["name"] + data["message"]))
                    utils.shake_sleep()
                else:
                    logger.info(
                        "failed to sign in, maybe cookie need renew, response: {}", data)
                    # Config().clear_cookies()
                    raise SystemExit

    def read_posts(self):
        if self.task_do["bbs_read_posts"]:
            logger.info("task has finished~")
        else:
            logger.info("start to read post task......")
            for i in range(self.task_do["bbs_read_posts_num"]):
                response = self.s.get(url=setting.bbs_detail_url.format(
                    self.posts[i]['post_id']))
                data = response.json()
                if data["message"] == "OK":
                    logger.info("read : {} succeed".format(
                        self.posts[i]['subject']))
                utils.shake_sleep()

    def like_posts(self):
        if self.task_do["bbs_like_posts"]:
            logger.info("like post has finished~")
        else:
            logger.info("start to like task......")
            for i in range(self.task_do["bbs_like_posts_num"]):
                response = self.s.post(url=setting.bbs_like_url, json={
                    "post_id": self.posts[i]["post_id"], "is_cancel": False})
                data = response.json()
                if data["message"] == "OK":
                    logger.info("like: {} succeed".format(
                        self.posts[i]['subject']))
                if Config.mihoyobbs["bbs_unlike"] == True:
                    utils.shake_sleep()
                    response = self.s.post(url=setting.bbs_like_url, json={
                        "post_id": self.posts[i]["post_id"], "is_cancel": True})
                    data = response.json()
                    if data["message"] == "OK":
                        logger.info("unlike: {} succeed".format(
                            self.posts[i]['subject']))
                utils.shake_sleep()

    def share_posts(self):
        if self.task_do["bbs_share"]:
            logger.info("share task has finished~")
        else:
            logger.info("start to share task......")
            response = self.s.get(url=setting.bbs_share_url.format(
                self.posts[0]["post_id"]))
            data = response.json()
            if data["message"] == "OK":
                logger.info("share：{} succeed".format(
                    self.posts[0]['subject']))
            utils.shake_sleep()
