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
            "cookie": f"stuid={cfg.mihoyobbs_cookies['stuid']};stoken={cfg.mihoyobbs_cookies['stoken']}",
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

        self.cfg = cfg

        cycle_missions = {'continuous_sign': 1, 'view_post_0': 3, 'post_up_0': 5, 'share_post_0': 1}
        self.missions_todo = {'bbs_' + k: {'is_get_award': False, 'rest_happened_times': v}
                              for k, v in cycle_missions.items()}
        self.fill_tasks()
        self.posts = self.get_posts()

    def fill_tasks(self) -> None:
        logger.info("start to get tasks.")
        response = self.s.get(url=setting.bbs_tasks_list)
        data = response.json()
        if "err" in data["message"]:
            logger.warning(
                "get tasks failed, maybe cookie need to renew, response: {}", data)
            raise SystemExit
        else:
            self.today_get_coins = data["data"]["can_get_points"]
            self.today_have_getcoins = data["data"]["already_received_points"]
            self.total_points = data["data"]["total_points"]
            logger.info(
                f"{self.can_get_points} miyo-coin can be getten. check mission list.")
            for mission in data["data"]["states"]:
                mission_key = 'bbs_' + mission['mission_key']
                if mission_key in self.missions_todo:
                    self.missions_todo[mission_key]['is_get_award'] = mission["is_get_award"]
                    self.missions_todo[mission_key]['rest_happened_times'] -= mission["happened_times"]
                    if not mission["is_get_award"]:
                        logger.info('{} hasn`t finished, rest happen time: {}', mission_key,
                                    self.missions_todo[mission_key]['rest_happened_times'])

    def get_posts(self) -> list:
        logger.info("start to view posts......")
        result = []
        response = self.s.get(url=setting.bbs_list_url.format(26))
        data = response.json()
        max_post_need = max(mission['rest_happened_times'] for mission in self.missions_todo.values())
        for i in range(max_post_need):
            result.append({
                'post_id': data["data"]["list"][i]["post"]["post_id"],
                'subject': data["data"]["list"][i]["post"]["subject"]
            })
        logger.info("get {} posts".format(len(result)))
        return result

    def sign_in_bbs(self) -> None:
        config_sign_list = self.cfg.mihoyobbs.get("bbs_signin_list", [])
        sign_list = [bbs_cfg for bbs_cfg in setting.mihoyobbs_list if int(bbs_cfg['id']) in config_sign_list]

        logger.info("start to sign in......")
        for sign_cfg in sign_list:
            response = self.s.post(url=setting.bbs_sign_url.format(sign_cfg["id"]), data="")
            data = response.json()
            if data["message"] == 'OK':
                logger.info(str(sign_cfg["name"] + data["message"]))
                utils.shake_sleep()
            else:
                logger.warning("failed to sign in. response: {}", data)

    def view_posts(self):
        logger.info("start to read post task......")
        for i in range(self.missions_todo["bbs_view_post_0"]['rest_happened_times']):
            response = self.s.get(url=setting.bbs_detail_url.format(self.posts[i]['post_id']))
            data = response.json()
            if data["message"] == "OK":
                logger.info("read : {} ({}, {})", self.posts[i]['subject'], i,
                            self.missions_todo["bbs_view_post_0"]['rest_happened_times'])
            utils.shake_sleep()

    def up_posts(self) -> None:
        logger.info("start to like task......")
        rest_times = self.missions_todo["bbs_post_up_0"]['rest_happened_times']
        for i in range(rest_times):
            response = self.s.post(url=setting.bbs_like_url, json={
                "post_id": self.posts[i]["post_id"], "is_cancel": False})
            data = response.json()
            if data["message"] == "OK":
                logger.info("like: {} ({}/{})", self.posts[i]['subject'], i, rest_times)

            if self.cfg.mihoyobbs["bbs_post_up_cancel"]:
                utils.shake_sleep()
                response = self.s.post(url=setting.bbs_like_url, json={
                    "post_id": self.posts[i]["post_id"], "is_cancel": True})
                data = response.json()
                if data["message"] == "OK":
                    logger.info("cancel up: {} succeed.", self.posts[i]['subject'])
            utils.shake_sleep()

    def share_posts(self) -> None:
        logger.info("start to share task......")
        rest_times = self.missions_todo["bbs_share_post_0"]['rest_happened_times']
        for i in range(rest_times):
            response = self.s.get(url=setting.bbs_share_url.format(self.posts[i]["post_id"]))
            data = response.json()
            if data["message"] == "OK":
                logger.info("share：{} ({}/{})", self.posts[0]['subject'], i , rest_times)
            utils.shake_sleep()
