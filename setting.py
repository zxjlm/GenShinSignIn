
"""
File: setting.py
Project: GenshinSignIn
File Created: Thursday, 23rd September 2021 8:04:23 am
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Thursday, 23rd September 2021 4:58:07 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description:
"""

import os
mihoyobbs_salt = "fd3ykrh7o1j54g581upo1tvpam0dsgtf"
mihoyobbs_salt_web = "14bmu1mz0yuljprsfgpvjh3ju2ni468r"
mihoyobbs_salt_web_old = "h8w582wxwgqvahcdkpvdhbh2w9casgfl"

mihoyobbs_version = "2.7.0"  # Slat和Version相互对应
mihoyobbs_version_old = "2.3.0"

mihoyobbs_client_type = "2"  # 1为ios 2为安卓
mihoyobbs_client_type_web = "5"  # 4为pc web 5为mobile web

mihoyobbs_list = [{
    "id": "1",
    "forumId": "1",
    "name": "崩坏3",
    "url": "https://bbs.mihoyo.com/bh3/"
}, {
    "id": "2",
    "forumId": "26",
    "name": "原神",
    "url": "https://bbs.mihoyo.com/ys/"
}, {
    "id": "3",
    "forumId": "30",
    "name": "崩坏2",
    "url": "https://bbs.mihoyo.com/bh2/"
}, {
    "id": "4",
    "forumId": "37",
    "name": "未定事件簿",
    "url": "https://bbs.mihoyo.com/wd/"
}, {
    "id": "5",
    "forumId": "34",
    "name": "大别野",
    "url": "https://bbs.mihoyo.com/dby/"
}]

# Config Load之后run里面进行列表的选择
mihoyobbs_list_use = []
mihoyo_login_url = 'https://user.mihoyo.com/#/login/captcha'

# 米游社的API列表
bbs_stuid_cookie_url = "https://webapi.account.mihoyo.com/Api/cookie_accountinfo_by_loginticket?login_ticket={}"
bbs_stoken_cookie_url = "https://api-takumi.mihoyo.com/auth/api/getMultiTokenByLoginTicket?login_ticket={}&token_types=3&uid={}"
bbs_tasks_list = "https://bbs-api.mihoyo.com/apihub/sapi/getUserMissionsState"  # 获取任务列表
bbs_sign_url = "https://bbs-api.mihoyo.com/apihub/sapi/signIn?gids={}"  # post
bbs_list_url = "https://bbs-api.mihoyo.com/post/api/getForumPostList?forum_id={}&is_good=false&is_hot=false&page_size=20&sort_type=1"
bbs_detail_url = "https://bbs-api.mihoyo.com/post/api/getPostFull?post_id={}"
bbs_share_url = "https://bbs-api.mihoyo.com/apihub/api/getShareConf?entity_id={}&entity_type=1"
bbs_like_url = "https://bbs-api.mihoyo.com/apihub/sapi/upvotePost"  # post json

genshin_act_id = "e202009291139501"
genshin_account_info_url = "https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz=hk4e_cn"
genshin_signed_url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id={}"
genshin_is_sign_url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?act_id={}&region={}&uid={}"
genshin_sign_url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign"
genshin_cookie_refresh = 'https://api-takumi.mihoyo.com/auth/api/getCookieAccountInfoBySToken'

path = os.path.dirname(os.path.realpath(__file__))
