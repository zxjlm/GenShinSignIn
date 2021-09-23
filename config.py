import os
import json
import tools

enable_Config = True
mihoyobbs_Login_ticket = ""
mihoyobbs_Stuid = ""
mihoyobbs_Stoken = ""
mihoyobbs_Cookies = ""
mihoyobbs = {
    "bbs_Global": True,
    "bbs_Signin": True,
    "bbs_Signin_multi": True,
    # 1: honkai3rd 2: genshin 3: honkai2 4: shijian 5: main conmunity
    "bbs_Signin_multi_list": [2, 5],
    "bbs_Read_posts": True,
    "bbs_Like_posts": True,
    "bbs_Unlike_posts": True,
    "bbs_Share_posts": True,
}
genshin_Auto_sign = True
honkai3rd_Auto_sign = True

path = os.path.dirname(os.path.realpath(__file__)) + "/config"
config_Path = f"{path}/config.json"


def Load_config():
    with open(config_Path, "r") as f:
        data = json.load(f)
        global enable_Config
        global mihoyobbs_Login_ticket
        global mihoyobbs_Stuid
        global mihoyobbs_Stoken
        global mihoyobbs_Cookies
        global mihoyobbs
        global genshin_Auto_sign
        global honkai3rd_Auto_sign
        enable_Config = data["enable_Config"]
        mihoyobbs_Login_ticket = data["mihoyobbs_Login_ticket"]
        mihoyobbs_Stuid = data["mihoyobbs_Stuid"]
        mihoyobbs_Stoken = data["mihoyobbs_Stoken"]
        mihoyobbs_Cookies = data["mihoyobbs_Cookies"]
        mihoyobbs["bbs_Gobal"] = data["mihoyobbs"]["bbs_Global"]
        mihoyobbs["bbs_Signin"] = data["mihoyobbs"]["bbs_Signin"]
        mihoyobbs["bbs_Signin_multi"] = data["mihoyobbs"]["bbs_Signin_multi"]
        mihoyobbs["bbs_Signin_multi_list"] = data["mihoyobbs"]["bbs_Signin_multi_list"]
        mihoyobbs["bbs_Read_posts"] = data["mihoyobbs"]["bbs_Read_posts"]
        mihoyobbs["bbs_Like_posts"] = data["mihoyobbs"]["bbs_Like_posts"]
        mihoyobbs["bbs_Unlike"] = data["mihoyobbs"]["bbs_Unlike"]
        mihoyobbs["bbs_Share"] = data["mihoyobbs"]["bbs_Share"]
        genshin_Auto_sign = data["genshin_Auto_sign"]
        honkai3rd_Auto_sign = data["honkai3rd_Auto_sign"]
        f.close()
        tools.log.info("Config加载完毕")


def Save_config():
    with open(config_Path, "r+") as f:
        data = json.load(f)
        data["mihoyobbs_Login_ticket"] = mihoyobbs_Login_ticket
        data["mihoyobbs_Stuid"] = mihoyobbs_Stuid
        data["mihoyobbs_Stoken"] = mihoyobbs_Stoken
        f.seek(0)
        f.truncate()
        temp_Text = json.dumps(data, sort_keys=False,
                               indent=4, separators=(', ', ': '))
        f.write(temp_Text)
        f.flush()
        f.close()
        tools.log.info("Config保存完毕")


def Clear_cookies():
    with open(config_Path, "r+") as f:
        data = json.load(f)
        data["enable_Config"] = False
        data["mihoyobbs_Login_ticket"] = ""
        data["mihoyobbs_Stuid"] = ""
        data["mihoyobbs_Stoken"] = ""
        data["mihoyobbs_Cookies"] = ""
        f.seek(0)
        f.truncate()
        temp_Text = json.dumps(data, sort_keys=False,
                               indent=4, separators=(', ', ': '))
        f.write(temp_Text)
        f.flush()
        f.close()
        tools.log.info("Cookie删除完毕")
        exit(1)
