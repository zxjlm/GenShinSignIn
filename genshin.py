import time
import tools
import config
import random
import setting
from request import http


class genshin:
    def __init__(self) -> None:
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'DS': tools.Get_ds(web=True, web_old=True),
            'Origin': 'https://webstatic.mihoyo.com',
            'x-rpc-app_version': setting.mihoyobbs_Version_old,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.3.0',
            'x-rpc-client_type': setting.mihoyobbs_Client_type_web,
            'Referer': 'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.mihoyo.hyperion',
            "Cookie": config.mihoyobbs_Cookies,
            'x-rpc-device_id': tools.Get_deviceid()
        }
        self.acc_List = self.Getacc_list()
        if len(self.acc_List) != 0:
            self.sign_Give = self.Get_signgive()

    def Getacc_list(self) -> list:
        tools.log.info("get account list...")
        temp_List = []
        req = http.get(setting.genshin_Account_info_url,
                       headers=self.headers, verify=False)
        data = req.json()
        if data["retcode"] != 0:
            tools.log.warn("get account list failed")
            exit(1)
        for i in data["data"]["list"]:
            temp_List.append([i["nickname"], i["game_uid"], i["region"]])
        tools.log.info(f"get {len(temp_List)} accounts")
        return temp_List

    def Get_signgive(self) -> list:
        tools.log.info("get sign in awards...")
        req = http.get(setting.genshin_Signlisturl.format(
            setting.genshin_Act_id), headers=self.headers, verify=False)
        data = req.json()
        if data["retcode"] != 0:
            tools.log.warn("get sgin awards failed")
            print(req.text)
            exit(1)
        return data["data"]["awards"]

    def refresh_cookies(self):
        params = (
            ('stoken', config.mihoyobbs_Stoken),
            ('uid', config.mihoyobbs_Stuid),
        )
        response_cookie = http.get(setting.genshin_cookie_refresh,
                                   headers=self.headers, params=params, verify=False)
        self.headers['Cookie'] += '; cookie_token={}'.format(response_cookie.json()[
            'data']['cookie_token']) + ';account_id=26184553'

    def Is_sign(self, region: str, uid: str):
        self.refresh_cookies()
        url = setting.genshin_Is_signurl.format(
            setting.genshin_Act_id, region, uid)
        req = http.get(url, headers=self.headers, verify=False)
        data = req.json()
        if data["retcode"] != 0:
            tools.log.warn("get account sign in info failed")
            print(req.text)
            exit(1)
        return data["data"]

    def Sign_acc(self):
        if len(self.acc_List) != 0:
            for i in self.acc_List:
                tools.log.info(f"now sign in for account {i[0]}...")
                time.sleep(random.randint(2, 8))
                is_data = self.Is_sign(region=i[2], uid=i[1])
                if is_data["first_bind"] == True:
                    tools.log.warn(f"{i[0]} manual sign first")
                else:
                    sign_Days = is_data["total_sign_day"] - 1
                    if is_data["is_sign"] == True:
                        tools.log.info(
                            f"{i[0]} has signed~ award today is{tools.Get_item(self.sign_Give[sign_Days])}")
                    else:
                        time.sleep(random.randint(2, 8))
                        req = http.post(url=setting.genshin_Signurl, headers=self.headers,
                                        json={'act_id': setting.genshin_Act_id, 'region': i[2], 'uid': i[1]}, verify=False)
                        data = req.json()
                        if data["retcode"] == 0:
                            if sign_Days == 0:
                                tools.log.info(
                                    f"{i[0]} sign in successed~\r\naward today is{tools.Get_item(self.sign_Give[sign_Days])}")
                            else:
                                tools.log.info(
                                    f"{i[0]} sign in successed~\r\naward today is{tools.Get_item(self.sign_Give[sign_Days + 1])}")
                        elif data["retcode"] == -5003:
                            tools.log.info(
                                f"{i[0]} has signed~\r\n award today is {tools.Get_item(self.sign_Give[sign_Days])}")
                        else:
                            tools.log.warn("sign in failed")
                            print(req.text)
        else:
            tools.log.warn("no target account")


# g = genshin()
# g.Sign_acc()
