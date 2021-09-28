import os
import setting
from loader import logger
from config import Config
from functools import wraps
import asyncio
import json


def loop_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            result = func(*args, **kwargs)
            try:
                if result.upper() == 'Y':
                    return True
                elif result.upper() == 'N':
                    return False
                else:
                    raise Exception(func.__name__)
            except Exception as _e:
                logger.warning(f'错误的输入, 输入内容: {result}, 错误对象: {_e}')
    return wrapper


class Generator:
    def __init__(self) -> None:
        # self.cfg = Config('', auto_load=False)
        self.config_path = ''

    @staticmethod
    def check_file(file_name) -> str:
        file_path = setting.path + f'/config/config_{file_name}.json'
        logger.info(f'------> 正在检查文件 {file_path}')
        if os.path.exists(file_path):
            return ""
        return file_path

    def generate_file(self) -> bool:
        retry_times = 3
        for foo in range(retry_times):
            foo != 0 and logger.warning(f'该路径下存在同名文件. 重试{foo}/{retry_times-1}')
            print('配置文件的名称:')
            file_name = input()
            file_path = self.check_file(file_name)
            if file_path == "":
                continue
            else:
                self.config_path = file_path
                logger.info(f'生成文件 {file_path}')
                return True
        else:
            logger.error('达到最大重试次数')
            return False

    @loop_decorator
    def enable_mihoyobbs_tasks(self):
        """是否启用米游社任务队列
        """
        print('[1/3]启用米游社任务队列(包括签到和日常米游币任务) (Y/N) :')
        return input()

    @loop_decorator
    def enable_genshin_signin(self):
        """是否启用原神每日签到
        """
        print('[2/3]启用原神每日签到 (Y/N) :')
        return input()

    # @loop_decorator
    # def enable_mail(self):
    #     """是否启用邮件通知(仅当cookie失效时)
    #     """
    #     print('[3/3]如需启用邮件通知(仅当cookie失效时), 请在文件生成后, 手动进行配置.')
        # return input()

    @loop_decorator
    def enable_mihoyobbs_sign(self):
        print('[1/3][1/4]是否启用米游社签到 (Y/N) :')
        return input()

    @loop_decorator
    def enable_mihoyobbs_view_post(self):
        print('[1/3][2/4]是否启用米游社-看帖任务 (Y/N) :')
        return input()

    @loop_decorator
    def enable_mihoyobbs_up_post(self):
        print('[1/3][3/4]是否启用米游社-点赞任务 (Y/N) :')
        return input()

    @loop_decorator
    def enable_mihoyobbs_share_post(self):
        print('[1/3][4/4]是否启用米游社-分享任务 (Y/N) :')
        return input()

    def generate_cookie(self):
        print('[3/3]是否需要生成cookie (Y/N):')
        print('注意: 此操作将会使用play_wright唤醒浏览器')
        result = input()
        if result.upper() == 'Y':
            from login import simulator
            cookie_raw = asyncio.run(simulator('str'))
            return cookie_raw
        else:
            logger.warning('跳过生成cookie...')
            return ""

    def process(self):
        self.generate_file()
        Config.mihoyobbs['enable'] = self.enable_mihoyobbs_tasks()
        Config.mihoyobbs['bbs_signin'] = self.enable_mihoyobbs_sign()
        if Config.mihoyobbs['bbs_signin']:
            Config.mihoyobbs['bbs_signin_list'] = [2, 5]
        Config.mihoyobbs['bbs_view_post_0'] = self.enable_mihoyobbs_view_post()
        Config.mihoyobbs['bbs_post_up_0'] = self.enable_mihoyobbs_up_post()
        Config.mihoyobbs['bbs_share_post_0'] = self.enable_mihoyobbs_share_post()
        Config.mihoyobbs['bbs_post_up_cancel'] = False

        Config.genshin_auto_sign = self.enable_genshin_signin()

        # cookies = self.generate_cookie()
        Config.mihoyobbs_cookies_raw = self.generate_cookie()

        print('--------------> 邮件通知默认不设置, 但是配置文件中生成了对应的接口槽, 如有需要, 对比说明文件填写即可 <--------')
        print('文件生成中...')

        with open(self.config_path, "w") as f:
            json.dump(Config.to_dict(), f, indent=4)

        print('文件生成完毕~')


if __name__ == "__main__":
    p = Generator()
    p.process()
