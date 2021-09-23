from config import Config
from login import Login
from genshin import Genshin
import setting
import mihoyobbs
import utils
import urllib3
from loguru import logger
import requests
import platform
import glob
from argparse import ArgumentParser, RawDescriptionHelpFormatter
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = 0.2
module_name = "GenShinSignIn"


def main():
    version_string = (
        f"%(prog)s {__version__} \n"
        f"requests:  {requests.__version__} \n"
        f"Python:  {platform.python_version()} \n"
    )

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=f"{module_name} " f"(Version {__version__})",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=version_string,
        help="Display version information and dependencies.",
    )
    parser.add_argument(
        "--check-cookie",
        default=False,
        action="store_true",
        dest="check_cookie",
        help="Check cookie is effect.",
    )
    parser.add_argument(
        "--parser-cookie",
        default=False,
        action="store_true",
        dest="parser_cookie",
        help="parser cookie.",
    )
    parser.add_argument(
        "--check-configs",
        "-c",
        default=False,
        action="store_true",
        dest="check-configs",
        help="parser cookie.",
    )
    parser.add_argument(
        "--show-all-site",
        action="store_true",
        dest="show_site_list",
        default=False,
        help="Show all information of the apis in files.",
    )
    parser.add_argument(
        "--json",
        "-j",
        metavar="JSON_FILES",
        dest="json_files",
        type=str,
        nargs="+",
        default=None,
        help="Load data from a local JSON file.Accept plural " "files.",
    )
    parser.add_argument(
        "--email",
        "-e",
        metavar="EMAIL_ADDRESS_LIST",
        dest="emails",
        type=str,
        nargs="*",
        default="not send",
        help="Send email to mailboxes. You can order the "
        "addresses in cmd argument, default is "
        "in the file 'config.py'.",
    )
    parser.add_argument(
        "--timeout",
        action="store",
        metavar="TIMEOUT",
        dest="timeout",
        default=None,
        help="Time (in seconds) to wait for response to "
        "requests. "
        "Default timeout is 35s. "
        "A longer timeout will be more likely to "
        "get results from slow sites. "
        "On the other hand, this may cause a long "
        "delay to gather all results.",
    )

    args = parser.parse_args()

    config_files = glob.glob(setting.path + '/config/config_*.json')

    if args.check_cookie:
        for config_file in config_files:
            Login(config_file).is_cookies_expires()
        raise SystemExit

    if args.parser_cookie:
        for config_file in config_files:
            Login(config_file).cookie_process()
        raise SystemExit

    for config_file in config_files:
        logger.info(
            '****************** start to get config {} *********', config_file)
        process(config_file)


def process(config_file):
    cfg = Config(config_file)
    if cfg.enable_config == True:
        Login(config_file).cookie_process()
        # if cfg.mihoyobbs_login_ticket and cfg.mihoyobbs_stuid and cfg.mihoyobbs_stoken == "":

        #     utils.shake_sleep()
        if cfg.mihoyobbs["bbs_signin_multi"] == True:
            for i in cfg.mihoyobbs["bbs_signin_multi_list"]:
                for i2 in setting.mihoyobbs_list:
                    if i == int(i2["id"]):
                        setting.mihoyobbs_list_use.append(i2)
        else:
            for i in setting.mihoyobbs_list:
                if int(i["id"]) == 5:
                    setting.mihoyobbs_list_use.append(i)
        if cfg.mihoyobbs["bbs_global"] == True:
            bbs = mihoyobbs.MihoyoBBS(cfg)
            if bbs.task_do["bbs_sign"] and bbs.task_do["bbs_read_posts"] and bbs.task_do["bbs_like_posts"] and bbs.task_do["bbs_share"]:
                logger.info(
                    f"sign succeed {bbs.today_get_coins}, now has {bbs.total_points} miyo coin")
            else:
                if cfg.mihoyobbs["bbs_signin"] == True:
                    bbs.sign_in_bbs()
                if cfg.mihoyobbs["bbs_read_posts"] == True:
                    bbs.read_posts()
                if cfg.mihoyobbs["bbs_like_posts"] == True:
                    bbs.like_posts()
                if cfg.mihoyobbs["bbs_share"] == True:
                    bbs.share_posts()
                bbs.get_tasks()
                logger.info(
                    f"今天已经获得{bbs.today_have_getcoins}个米游币，还能获得{bbs.today_get_coins}个米游币，目前有{bbs.total_points}个米游币")
                utils.shake_sleep()
        else:
            logger.info("米游社功能未启用！")
        # 原神签到
        if(cfg.genshin_auto_sign == True):
            logger.info("正在进行原神签到")
            g = Genshin(cfg)
            g.main()
            utils.shake_sleep()
        else:
            logger.info("原神签到功能未启用！")
    else:
        logger.warn("Config未启用！")


if __name__ == "__main__":
    main()
