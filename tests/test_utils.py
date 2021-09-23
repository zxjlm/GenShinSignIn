'''
File: utils_test.py
Project: leisureliness
File Created: Thursday, 23rd September 2021 5:10:09 pm
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Thursday, 23rd September 2021 5:10:13 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description: 
'''

import utils


def test_split_cookies():
    cookies_expamle = ('AlteonP=AHowIfM=BAQrP1dtgaRXlJg$$; '
                       'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217c0ca15710454-0958487b0c6e68-a7d173c'
                       '-2073600-17c0ca157117af%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%'
                       '24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22'
                       '%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC;'
                       'AlteonP=AMaaD/MBAQ==plboZ+vMvQEw$$; SESSION=d5d8aaa0-8984-48f8-8cb3-bf392ee513c4')
    cookie_dict = utils.split_cookies(cookies_expamle)
    assert cookie_dict['AlteonP'] == 'AMaaD/MBAQ==plboZ+vMvQEw$$'
    assert cookie_dict.keys().__len__() == 3


def test_generate_md5():
    assert utils.generate_md5('9527') == '52569c045dc348f12dfc4c85000ad832'


def test_get_timestamp():
    assert len(utils.get_timestamp()) == 10
    assert len(utils.get_timestamp('js')) == 13

