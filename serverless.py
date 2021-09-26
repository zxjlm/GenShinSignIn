# -*- coding: utf-8 -*-
import logging
from utils import get_python_version
import glob
import setting
from main import process

# if you open the initializer feature, please implement the initializer function, as below:
# def initializer(context):
#   logger = logging.getLogger()
#   logger.info('initializing')


def handler(event, context):
    logger = logging.getLogger()
    logger.info(get_python_version())
    config_files = glob.glob(setting.path + '/config/config_*.json')
    for config_file in config_files:
        logger.info(f'****************** start to get config {config_file} *********')
        process(config_file)
