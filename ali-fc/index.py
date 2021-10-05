# -*- coding: utf-8 -*-
import logging
import glob
import os
# from ..main import process
from main import process

# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
# def initializer(context):
#   logger = logging.getLogger()
#   logger.info('initializing')


def handler(event, context):
    logger = logging.getLogger()

    path = os.path.dirname(os.path.realpath(__file__))
    config_files = glob.glob(path + '/../config/config_*.json')
    logger.warning(config_files)

    for config_file in config_files:
        logger.info(
            '****************** start to get config {} *********'.format(config_file))
        process(config_file)
    return 'success'
